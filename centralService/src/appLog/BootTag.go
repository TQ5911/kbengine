package appLog

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime/debug"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ============================================================================
//  统一启动日志 TAG
//
//  为什么需要它
//    线上中心服被 systemd（Restart=always）拉起时，运维侧要能"立刻知道哪个服务
//    重启了、这是第几次、上一次是不是崩的"。原先每个服务的启动日志措辞不一致
//    （"server is running" / 各自的中文串），没法写一条通用告警规则，只能逐服务
//    配置。
//
//    本模块给 12 个中心服输出同一行格式的启动日志，所有服务共用同一个 TAG
//    CENTRALSVC_BOOT，采集侧匹配这一个词即可覆盖全部服务。
//
//  一行长这样
//    2026-11-02T17:05:12.345+0800 INFO CENTRALSVC_BOOT phase=ready service=maple
//      serverName=mapleServer serverId=1 instid=0 pid=12345 host=ip-172-16-41-49
//      boot=3 prev=unclean
//
//  字段
//    tag        固定为 CENTRALSVC_BOOT，可用环境变量 CENTRALSVC_BOOT_TAG 覆盖
//    phase      starting | ready | failed | exit   （含义见下）
//    service    服务名。取「可执行文件所在目录名」，与 deploy/instances.conf 的
//               name 列严格一致（配置文件名也是按这个规则推导的，见 common.GetConfig）
//    serverName 配置里的 serverName（可能为空，配置没读到就没有该字段）
//    serverId   配置里的 serverId
//    instid     启动参数 --instid，默认取 pid（与 Pidfile 的默认值一致）
//    pid        进程号
//    host       主机名，多机部署时用于区分是哪台机器
//    boot       本机本实例累计第几次启动。>1 说明发生过重启
//    prev       上一次退出的干净程度：clean / unclean / none(首次启动)
//                  clean   上次走的是信号处理的优雅退出（systemctl stop/restart）
//                  unclean 上次没留 clean 标记，即 panic / OOM / SIGKILL / 启动失败
//
//  phase 的四个取值
//    starting  进程已进入 main，配置还没读。这一行只用 stdout 输出（此时 zap
//              尚未初始化，写不了业务日志文件），但配置完全读不到时它是唯一能
//              证明"进程确实被拉起来了"的证据
//    ready     所有监听端口 Listen 成功，服务真正可用了 → 告警主匹配点
//    failed    任一初始化阶段失败，带 reason=。启动失败比启动成功更需要告警
//    exit      进程退出，带 code= 与 reason=。和下一次的 starting 配对就能看出
//              "挂了多久才被拉起"
//
//  双路输出
//    业务日志文件（zap/lumberjack，<服务名>.log）与 stdout 各写一份。
//    stdout 在 systemd 里落到 journald 或 <服务名>.out.log（取决于 deploy.env 的
//    LOG_STDOUT_MODE）。这样无论日志采集走文件还是走 journal，都能拿到 TAG。
//
//  boot / prev 的状态文件
//    写在进程工作目录（与 pid 文件同目录，WorkingDirectory 由 systemd 保证）：
//      <服务名>_<instid>.boot   累计启动次数
//      <服务名>_<instid>.clean  优雅退出标记，读取后即删除
//    读写失败一律忽略，只让 boot=0 / prev 退化成 unclean 之外的保守值，
//    绝不允许日志打点把服务本身搞挂。
// ============================================================================

const (
	// DefaultBootTag 所有中心服共用的启动日志 TAG
	DefaultBootTag = "CENTRALSVC_BOOT"

	// BootTagEnvKey 覆盖 TAG 名，例如灰度期想单独抓某一批服务
	BootTagEnvKey = "CENTRALSVC_BOOT_TAG"

	// BootServiceEnvKey 覆盖服务名。默认按可执行文件目录名推导，
	// 只有在非常规部署（二进制不在 <服务名>/ 目录下）时才需要设置
	BootServiceEnvKey = "CENTRALSVC_SERVICE"

	// BootPhaseStarting 进程启动，配置尚未加载
	BootPhaseStarting = "starting"
	// BootPhaseReady 端口全部监听成功，服务可用
	BootPhaseReady = "ready"
	// BootPhaseFailed 初始化或监听失败
	BootPhaseFailed = "failed"
	// BootPhaseExit 进程退出
	BootPhaseExit = "exit"
)

var (
	bootOnce      sync.Once
	bootBeginOnce sync.Once

	// 以下字段在 bootOnce 里一次性初始化，之后只读
	bootService string
	bootInstID  string
	bootCount   int
	bootPrev    string
	bootHost    string

	// 配置里的服务名/ID，由 base.initLog 在配置读到之后回填
	bootServerMu   sync.RWMutex
	bootServerName string
	bootServerID   int
	bootServerSet  bool
)

// BootTag 返回当前生效的启动 TAG
func BootTag() string {
	if v := strings.TrimSpace(os.Getenv(BootTagEnvKey)); v != "" {
		return v
	}
	return DefaultBootTag
}

// SetBootServerInfo 由 base.initLog 在配置加载成功后调用，把 serverName/serverId
// 补进后续的 TAG 行。starting 那行发生在配置之前，所以没有这两个字段。
func SetBootServerInfo(name string, id int) {
	bootServerMu.Lock()
	defer bootServerMu.Unlock()
	bootServerName = name
	bootServerID = id
	bootServerSet = true
}

// BootBegin 在 main 进入初始化流程的最开头调用，phase=starting。
// 此时日志系统还没起来，只能走 stdout。
//
// 幂等：base.Init 里也会调一次，提前在 main 调过的服务不会打出两条 starting。
func BootBegin() {
	bootBeginOnce.Do(func() {
		bootEmit(BootPhaseStarting)
	})
}

// BootFatalRecover 用在 main 的第一行（defer），兜住 base.Init 之前的 panic。
//
// 背景：centralLogin / queueServer 在 main 里先读 serverList.json，读不到就
// log.Panicf。这一步发生在 base.Init 之前 —— 日志系统和 common.Run 的 recover
// 都还没就位，线上表现为"进程起来了又立刻消失，日志里一个 TAG 都没有"，
// 恰好是最该告警的场景。用它把 panic 变成 failed + exit 两条 TAG。
//
// 正常返回时什么都不做，退出打点仍由 ExitProgram 负责。
func BootFatalRecover() {
	r := recover()
	if r == nil {
		return
	}
	// 此刻 logger 可能还是 nil，堆栈直接写 stderr，保证 journal / out.log 里有现场
	_, _ = fmt.Fprintf(os.Stderr, "main panic: %v\n%s\n", r, string(debug.Stack()))
	BootFailed("panic", "stage=main")
	BootExit(1, "panic")
	os.Exit(1)
}

// BootReady 在全部监听端口 Listen 成功后调用，phase=ready。
// 这是告警侧的主匹配点：出现这一行说明服务确实提供过服务。
func BootReady() {
	bootEmit(BootPhaseReady)
}

// BootFailed 在任一初始化阶段失败时调用，phase=failed。
//
// reason 用 snake_case 短语，不要带空格（空格会破坏 kv 解析），
// 例如 init_config / init_log / init_report / listen / write_pid_file。
func BootFailed(reason string, extra ...string) {
	bootEmit(BootPhaseFailed, append([]string{"reason=" + normalizeValue(reason)}, extra...)...)
}

// BootExit 在进程退出时调用，phase=exit。
// reason 同样避免空格，例如 sigterm / sigint / panic / load_data。
func BootExit(code int, reason string, extra ...string) {
	fields := []string{"code=" + strconv.Itoa(code)}
	if reason != "" {
		fields = append(fields, "reason="+normalizeValue(reason))
	}
	bootEmit(BootPhaseExit, append(fields, extra...)...)
}

// MarkCleanExit 写入优雅退出标记，下一次启动时 prev 就会是 clean。
// 只有正常退出（信号处理走 ExitProgram(0/130)）才应该调用；
// panic、OOM、SIGKILL 都到不了这里，于是下次启动 prev=unclean。
func MarkCleanExit() {
	initBootState()
	_ = os.WriteFile(bootStatePath("clean"), []byte(strconv.FormatInt(time.Now().Unix(), 10)), 0644)
}

// bootEmit 组装并输出一行启动日志：stdout 一定有，zap 就绪时再多写一份文件。
func bootEmit(phase string, extra ...string) {
	initBootState()

	// 用切片的字面量顺序保证字段出现次序稳定，采集侧正则才好写
	fields := make([]string, 0, 16)
	fields = append(fields, BootTag())
	fields = append(fields, "phase="+phase)
	fields = append(fields, "service="+normalizeValue(bootService))

	bootServerMu.RLock()
	if bootServerSet {
		fields = append(fields, "serverName="+normalizeValue(bootServerName))
		fields = append(fields, "serverId="+strconv.Itoa(bootServerID))
	}
	bootServerMu.RUnlock()

	fields = append(fields, "instid="+normalizeValue(bootInstID))
	fields = append(fields, "pid="+strconv.Itoa(os.Getpid()))
	fields = append(fields, "host="+normalizeValue(bootHost))
	fields = append(fields, "boot="+strconv.Itoa(bootCount))
	fields = append(fields, "prev="+bootPrev)
	fields = append(fields, extra...)

	line := strings.Join(fields, " ")

	// 1) stdout：systemd 收走，落到 journald 或 <服务名>.out.log
	//    时间格式与 zap 的 ISO8601TimeEncoder 对齐，方便两路日志混在一起看
	stamp := time.Now().Format("2006-01-02T15:04:05.000Z0700")
	_, _ = os.Stdout.WriteString(stamp + " INFO " + line + "\n")

	// 2) 业务日志文件：LogInit 之后 logger 才非空，在此之前跳过
	if logger != nil {
		logger.Info(line)
	}
}

// initBootState 一次性初始化服务名、实例号、启动次数、上次退出状态
func initBootState() {
	bootOnce.Do(func() {
		bootService = detectServiceName()
		bootInstID = detectInstID()
		bootHost, _ = os.Hostname()
		bootCount, bootPrev = nextBootCount()
	})
}

// detectServiceName 推导服务名。
//
// 优先取 os.Args[0] 的目录名：这和 common.GetConfig() 推导配置文件名
// <服务名>.json 用的是同一套规则，两者必须同源，否则 TAG 里的服务名会和
// 实际加载的配置对不上。
func detectServiceName() string {
	if v := strings.TrimSpace(os.Getenv(BootServiceEnvKey)); v != "" {
		return v
	}
	if len(os.Args) > 0 {
		if name := cleanDirName(os.Args[0]); name != "" {
			return name
		}
	}
	if exe, err := os.Executable(); err == nil {
		if name := cleanDirName(exe); name != "" {
			return name
		}
	}
	return "unknown"
}

func cleanDirName(path string) string {
	name := filepath.Base(filepath.Dir(path))
	if name == "" || name == "." || name == string(filepath.Separator) {
		return ""
	}
	return name
}

// detectInstID 从启动参数里取 --instid，取不到就用 pid。
// 默认值与 common.InitFlag 的默认值保持一致（同样是 os.Getpid()），
// 这样 boot 状态文件与 pid 文件的 <服务名>_<instid> 前缀是一致的。
func detectInstID() string {
	for i, arg := range os.Args {
		if v, ok := flagValue(arg, "instid"); ok {
			return v
		}
		// 兼容 "--instid 0" 这种空格分隔写法
		if (arg == "--instid" || arg == "-instid") && i+1 < len(os.Args) {
			return os.Args[i+1]
		}
	}
	return strconv.Itoa(os.Getpid())
}

func flagValue(arg, name string) (string, bool) {
	for _, prefix := range []string{"--" + name + "=", "-" + name + "="} {
		if strings.HasPrefix(arg, prefix) {
			return strings.TrimPrefix(arg, prefix), true
		}
	}
	return "", false
}

// bootStatePath 返回 boot / clean 状态文件的绝对路径（与 pid 文件同在 CWD）
func bootStatePath(suffix string) string {
	name := bootService + "_" + bootInstID + "." + suffix
	if wd, err := os.Getwd(); err == nil {
		return filepath.Join(wd, name)
	}
	return name
}

// nextBootCount 读取并自增启动次数，同时判断上次退出是否干净。
//
// prev 的判定逻辑：
//   - boot 文件不存在           → none，这是第一次启动
//   - clean 标记存在            → clean，上次是优雅退出，顺手删掉标记
//   - 其余                      → unclean，上次 panic / OOM / SIGKILL / 启动失败
func nextBootCount() (count int, prev string) {
	bootPath := bootStatePath("boot")

	exists := false
	if b, err := os.ReadFile(bootPath); err == nil {
		exists = true
		if n, e := strconv.Atoi(strings.TrimSpace(string(b))); e == nil && n > 0 {
			count = n
		}
	}
	count++
	// 写失败不影响服务，最多下次 boot 又从 1 开始
	_ = os.WriteFile(bootPath, []byte(strconv.Itoa(count)), 0644)

	cleanPath := bootStatePath("clean")
	cleanExists := false
	if _, err := os.Stat(cleanPath); err == nil {
		cleanExists = true
		_ = os.Remove(cleanPath)
	}

	switch {
	case !exists:
		prev = "none"
	case cleanExists:
		prev = "clean"
	default:
		prev = "unclean"
	}
	return count, prev
}

// NormalizeField 供调用方拼 key=value 字段时复用同一套转义规则。
// 对已经规范过的值再调用一次是幂等的。
func NormalizeField(v string) string {
	return normalizeValue(v)
}

// normalizeValue 把会破坏 key=value 结构的字符替换掉，
// 避免一个带空格的 serverName 把后面的字段解析全部带偏。
func normalizeValue(v string) string {
	if v == "" {
		return "-"
	}
	replacer := strings.NewReplacer(" ", "_", "\t", "_", "\n", "_", "\r", "_", "\"", "")
	return replacer.Replace(v)
}
