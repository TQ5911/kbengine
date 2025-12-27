
"""
零依赖、Python 3.7+ 可用的超高精度埋点计时器
新增：支持一段代码内连续打多个时间戳（链式或 with）
"""
import time, statistics, collections, contextlib

__all__ = ['spot', 'Span']  # 只导出这两个

# ---------- 内部工具 ----------
def _now():
    return time.perf_counter()

class _Spot:
    __slots__ = ('_data',)
    def __init__(self):
        self._data = collections.defaultdict(list)

    # ---------- 老接口：全局 start/stop ----------
    def start(self, key: str):
        return key, _now()

    def stop(self, key: str, handle):
        _key, t0 = handle
        if _key != key:
            raise ValueError('key mismatch')
        self._data[key].append(_now() - t0)

    # ---------- 老接口：with ----------
    @contextlib.contextmanager
    def __call__(self, key: str):
        t0 = _now()
        try:
            yield
        finally:
            self._data[key].append(_now() - t0)

    # ---------- 新接口：生成一个 Span ----------
    def span(self, key: str):
        return Span(key, self._data)

    # ---------- 报表 / 清零（同旧） ----------
    def report(self, *, nanoseconds=False):
        unit = 'ns' if nanoseconds else 'us'
        factor = 1e9 if nanoseconds else 1e6
        lines = []
        for k in sorted(self._data):
            samples = self._data[k]
            n = len(samples)
            if n == 0:
                continue
            mean = statistics.mean(samples) * factor
            stdev = statistics.stdev(samples) * factor if n > 1 else 0.0
            lines.append(f'{k:20s}  n={n:8d}  mean={mean:8.1f} {unit}  stdev={stdev:6.1f} {unit}')
        return '\n'.join(lines) if lines else '(no samples)'

    def clear(self, key=None):
        if key is None:
            self._data.clear()
        else:
            self._data.pop(key, None)


# 全局单例
spot = _Spot()
