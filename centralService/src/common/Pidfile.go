package common

import (
	"centralService/src/appLog"
	"flag"
	"io/ioutil"
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
	return serverName + "_" + instID + ".pid"
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
	err = ioutil.WriteFile(pidFilePath, strByte, 0644)
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
				ExitProgram(130)
			case syscall.SIGHUP, syscall.SIGTERM, syscall.SIGQUIT:
				ExitProgram(0)
			default:
				appLog.Errorf("catched kill unknown signal %d\n", s)
			}
		}
	}()
}

func ExitProgram(exitCode int) {
	appLog.Infof("Exit Process, exitCode=%d\n", exitCode)
	ok := DelPidFile()
	if !ok {
		exitCode = 128
	}
	if exitCode != 0 && exitCode != 130 {
		appLog.Infof("Process exited with code %d\n", exitCode)
	}
	os.Exit(exitCode)
}
