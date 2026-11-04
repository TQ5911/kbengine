package common

import (
	"centralService/src/appLog"
	"flag"
	"os"
	"os/signal"
	"path/filepath"
	"strconv"
	"syscall"
)

var instID string
var pidDirPath string
var serverName string
var serverID int

func InitFlag() {
	flag.StringVar(&instID, "instid", strconv.Itoa(os.Getpid()), "tencent inst id")
	flag.StringVar(&pidDirPath, "pidpath", ".", "pid file writen path")
}

func InitAndParseFlag() {
	InitFlag()
	flag.Parse()
}

func GetPidFile() string {
	exePath, err := os.Executable()
	if err != nil {
		panic(err)
	}
	return filepath.Base(exePath) + "_" + instID + ".pid"
}

func GetServerName() string {
	return serverName
}

func GetServerID() int {
	return serverID
}

func SetServerName(sName string) {
	serverName = sName
}

func SetServerID(sID int) {
	serverID = sID
}

func GetPidFilePath() string {
	pidDirAbsPath, err := filepath.Abs(pidDirPath)
	if err != nil {
		return filepath.Join(pidDirPath, GetPidFile())
	} else {
		return filepath.Join(pidDirAbsPath, GetPidFile())
	}
}

func WritePidFile() bool {
	pid := os.Getpid()
	pidFilePath := GetPidFilePath()
	_, err := os.Lstat(pidFilePath)
	if !os.IsNotExist(err) {
		appLog.Errorf("WritePidFile fail, pidFile already Exist %s\n", pidFilePath)
		return false
	}

	strByte := []byte(strconv.Itoa(pid))
	err = os.WriteFile(pidFilePath, strByte, 0644)
	if err != nil {
		appLog.Errorf("WritePidFile fail, pidFile write broken %s, err=%v\n", pidFilePath, err)
		return false
	}

	appLog.Infof("write pidFile %s, pid=%d\n", pidFilePath, pid)
	return true
}

func DelPidFile() bool {
	pidFilePath := GetPidFilePath()
	_, err := os.Lstat(pidFilePath)
	if os.IsNotExist(err) {
		appLog.Errorf("DelPidFile fail, pidFile not Exist %s\n", pidFilePath)
		return false
	}

	err = os.Remove(pidFilePath)
	if err != nil {
		appLog.Errorf("DelPidFile fail, pidFile delete broken %s, err=%v\n", pidFilePath, err)
		return false
	}
	appLog.Infof("delete pidFile %s\n", pidFilePath)
	return true
}

func StartListenKillSignal() {
	c := make(chan os.Signal, 1)

	listenedSingals := []os.Signal{syscall.SIGHUP, syscall.SIGINT, syscall.SIGTERM, syscall.SIGQUIT}
	signal.Notify(c, listenedSingals...)
	appLog.Infof("start listen kill signal %v\n", listenedSingals)
	go func() {
		for s := range c {
			switch s {
			case syscall.SIGINT:
				// 130 = 128+SIGINT，沿用原有退出码语义
				ExitProgram(130, "sigint")
			case syscall.SIGHUP, syscall.SIGTERM, syscall.SIGQUIT:
				ExitProgram(0, signalName(s))
			default:
				appLog.Errorf("catched kill unknown signal %d\n", s)
			}
		}
	}()
}

// signalName 把信号转成可放进日志字段的小写短名
func signalName(s os.Signal) string {
	switch s {
	case syscall.SIGHUP:
		return "sighup"
	case syscall.SIGTERM:
		return "sigterm"
	case syscall.SIGQUIT:
		return "sigquit"
	case syscall.SIGINT:
		return "sigint"
	default:
		return "signal"
	}
}

// ExitProgram 退出进程，并在退出前打一条 phase=exit 的启动 TAG。
//
// reason 可选，用于说明退出原因（信号名 / panic / 业务失败），
// 会原样出现在 reason= 字段里，不要带空格。
func ExitProgram(exitCode int, reason ...string) {
	appLog.Infof("Exit Process, exitCode=%d\n", exitCode)

	// 先记录原始退出码：下面 DelPidFile 失败会把 exitCode 改成 128
	origCode := exitCode

	ok := DelPidFile()
	if !ok {
		exitCode = 128
	}
	if exitCode != 0 && exitCode != 130 {
		appLog.Infof("Process exited with code %d\n", exitCode)
	}

	r := "unspecified"
	if len(reason) > 0 && reason[0] != "" {
		r = reason[0]
	}
	appLog.BootExit(origCode, r)

	// 只有正常退出才写 clean 标记，下一次启动的 prev 才会是 clean。
	// panic 走 exitCode=1、被 SIGKILL/OOM 则根本到不了这里，这两种情况
	// 下次启动会看到 prev=unclean，正是需要告警的"挂掉后被拉起"。
	if origCode == 0 || origCode == 130 {
		appLog.MarkCleanExit()
	}

	os.Exit(exitCode)
}
