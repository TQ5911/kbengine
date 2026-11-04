package appLog

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// 这些 key 由测试自己控制，需要从父进程环境里剔掉，避免继承的残留值覆盖断言
var bootTagChildEnvKeys = []string{
	"CENTRALSVC_BOOTTAG_CHILD",
	"CENTRALSVC_BOOTTAG_MODE",
	"CENTRALSVC_SERVICE",
	"CENTRALSVC_BOOT_TAG",
}

func isBootTagChild() bool {
	return os.Getenv("CENTRALSVC_BOOTTAG_CHILD") == "1"
}

// TestBootTagLifecycle 验证启动 TAG 的完整生命周期语义：
// 首次启动 prev=none → 崩溃后拉起 prev=unclean → 优雅退出后拉起 prev=clean，
// 同时 boot 计数逐次递增。
//
// 因为 boot 状态是 sync.Once 初始化的进程级状态，这里用「父进程拉起子进程」的
// 方式模拟多次真实启动，每次子进程 CWD 指向同一个临时目录，boot/clean 文件因此累积。
func TestBootTagLifecycle(t *testing.T) {
	if isBootTagChild() {
		runBootTagChild()
		return
	}

	dir := t.TempDir()
	env := map[string]string{"CENTRALSVC_SERVICE": "maple"}

	// 第 1 次启动：首次，正常 ready 后模拟崩溃退出（不写 clean）
	out := runBootTagChildProcess(t, dir, "ready", env)
	for _, want := range []string{
		"phase=starting", "phase=ready", "service=maple", "boot=1", "prev=none",
	} {
		if !strings.Contains(out, want) {
			t.Fatalf("第 1 次启动输出缺少 %q\n实际输出:\n%s", want, out)
		}
	}

	// 第 2 次启动：上次没留 clean 标记 → prev=unclean，boot 递增
	out = runBootTagChildProcess(t, dir, "ready", env)
	t.Logf("启动 TAG 实际输出:\n%s", out)
	for _, want := range []string{"boot=2", "prev=unclean"} {
		if !strings.Contains(out, want) {
			t.Fatalf("第 2 次启动输出缺少 %q\n实际输出:\n%s", want, out)
		}
	}

	// 第 3 次启动：这次优雅退出，写 clean 标记
	runBootTagChildProcess(t, dir, "ready-clean", env)

	// 第 4 次启动：上一次干净退出 → prev=clean
	out = runBootTagChildProcess(t, dir, "ready", env)
	for _, want := range []string{"boot=4", "prev=clean"} {
		if !strings.Contains(out, want) {
			t.Fatalf("第 4 次启动输出缺少 %q\n实际输出:\n%s", want, out)
		}
	}

	// failed 分支：reason 必须能打到日志里，否则启动失败无法定位
	out = runBootTagChildProcess(t, dir, "fail", env)
	for _, want := range []string{"phase=failed", "reason=init_config", "boot=5"} {
		if !strings.Contains(out, want) {
			t.Fatalf("failed 分支输出缺少 %q\n实际输出:\n%s", want, out)
		}
	}

	// boot 状态文件应落在子进程 CWD，且计数与启动次数一致
	b, err := os.ReadFile(filepath.Join(dir, "maple_0.boot"))
	if err != nil {
		t.Fatalf("boot 状态文件未生成: %v", err)
	}
	if got := strings.TrimSpace(string(b)); got != "5" {
		t.Fatalf("boot 状态文件计数应为 5，实际 %q", got)
	}
}

// TestBootTagServiceNameFromExeDir 验证 service 字段默认按「可执行文件所在目录名」
// 推导 —— 生产上 os.Args[0] 是 <安装根>/<服务名>/<服务名>，这个规则必须和
// common.GetConfig() 推导 <服务名>.json 的规则一致，否则 TAG 里的服务名会和
// 实际加载的配置对不上。
func TestBootTagServiceNameFromExeDir(t *testing.T) {
	if isBootTagChild() {
		runBootTagChild()
		return
	}

	// 不设 CENTRALSVC_SERVICE，让代码走自动推导
	out := runBootTagChildProcess(t, t.TempDir(), "ready", nil)

	want := "service=" + filepath.Base(filepath.Dir(os.Args[0]))
	if !strings.Contains(out, want) {
		t.Fatalf("service 未按可执行文件目录名推导，期望包含 %q\n实际输出:\n%s", want, out)
	}
}

// TestBootTagWritesBusinessLog 验证 TAG 同时写进业务日志文件（zap/lumberjack），
// 保证采集侧无论走文件还是走 stdout 都能匹配到。
func TestBootTagWritesBusinessLog(t *testing.T) {
	if isBootTagChild() {
		runBootTagChild()
		return
	}

	dir := t.TempDir()
	runBootTagChildProcess(t, dir, "ready-log", map[string]string{"CENTRALSVC_SERVICE": "maple"})

	b, err := os.ReadFile(filepath.Join(dir, "child.log"))
	if err != nil {
		t.Fatalf("业务日志文件未生成: %v", err)
	}
	logText := string(b)
	for _, want := range []string{
		"CENTRALSVC_BOOT", "phase=ready", "service=maple", "serverName=mapleServer", "serverId=1",
	} {
		if !strings.Contains(logText, want) {
			t.Fatalf("业务日志缺少 %q\n实际内容:\n%s", want, logText)
		}
	}
}

// runBootTagChild 在子进程中按 MODE 走一遍启动流程，并用不同退出方式模拟
// 「崩溃」与「优雅退出」，让父进程能从下一次启动的 prev 字段观察到差别。
func runBootTagChild() {
	// BootBegin 会从 os.Args 里取 --instid，但 testing 已经解析过 flag，
	// 不能真的把 --instid 传给测试二进制，这里在调用前直接补进 os.Args。
	// 固定为 0，与 systemd 的 --instid=0 一致，boot 状态文件名才稳定。
	os.Args = append(os.Args, "--instid=0")

	BootBegin()
	switch os.Getenv("CENTRALSVC_BOOTTAG_MODE") {
	case "ready":
		BootReady()
		// 不写 clean 标记，等价于 panic / OOM / SIGKILL
		os.Exit(1)
	case "ready-clean":
		BootReady()
		MarkCleanExit()
		os.Exit(0)
	case "ready-log":
		// 模拟真实顺序：BootBegin 已经在上面打过（logger 还是 nil），
		// 之后 LogInit 起来，ready 就是「文件 + stdout」双路
		if !LogInit("child.log", 0, 10) {
			os.Exit(4)
		}
		SetBootServerInfo("mapleServer", 1)
		BootReady()
		Sync()
		os.Exit(0)
	case "fail":
		BootFailed("init_config")
		os.Exit(2)
	default:
		os.Exit(3)
	}
}

func runBootTagChildProcess(t *testing.T, dir, mode string, extraEnv map[string]string) string {
	t.Helper()

	cmd := exec.Command(os.Args[0], "-test.run="+t.Name())
	cmd.Dir = dir
	cmd.Env = childEnv(extraEnv, mode)

	out, _ := cmd.CombinedOutput()
	return string(out)
}

// childEnv 从父进程环境里剔掉测试自己控制的 key，再叠加本次要设的值，
// 避免同名变量重复出现时 os.Getenv 取到父进程的旧值。
func childEnv(extra map[string]string, mode string) []string {
	env := make([]string, 0, len(os.Environ())+len(extra)+2)
	for _, kv := range os.Environ() {
		skip := false
		for _, key := range bootTagChildEnvKeys {
			if strings.HasPrefix(kv, key+"=") {
				skip = true
				break
			}
		}
		if !skip {
			env = append(env, kv)
		}
	}
	env = append(env, "CENTRALSVC_BOOTTAG_CHILD=1", "CENTRALSVC_BOOTTAG_MODE="+mode)
	for k, v := range extra {
		env = append(env, k+"="+v)
	}
	return env
}
