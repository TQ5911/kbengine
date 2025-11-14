package appLog

import (
	"centralService/src/common/report"
	"encoding/json"
	"fmt"
	"log"

	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var logger *zap.SugaredLogger

const (
	DEFAULT_LOG_LEVEL       = zapcore.InfoLevel
	DEFAULT_LOG_ROTATE_SIZE = 500
)

var LOG_LEVEL_CFG = map[int]zapcore.Level{-1: zapcore.DebugLevel, 0: zapcore.InfoLevel, 1: zapcore.WarnLevel, 2: zapcore.ErrorLevel, 3: zapcore.DPanicLevel, 4: zapcore.PanicLevel, 5: zapcore.FatalLevel}

func LogInit(logPath string, logLevel int, logRotateSize int) bool {
	if len(logPath) == 0 {
		log.Println("log path is empty~")
		return false
	}
	zapLevel, ok := LOG_LEVEL_CFG[logLevel]
	if !ok {
		log.Printf("unknow log level~level:%v, valid log levels:%v", logLevel, LOG_LEVEL_CFG)
		return false
	}
	logger = newSugaredLogger(logPath, logRotateSize, zapLevel)
	return true
}

func newSugaredLogger(logPath string, logRotateSize int, logLevel zapcore.Level) *zap.SugaredLogger {
	logger := newLogger(logPath, logRotateSize, logLevel)
	return logger.Sugar()
}

func newLogger(logPath string, logRotateSize int, logLevel zapcore.Level) *zap.Logger {
	level := zap.NewAtomicLevelAt(logLevel)

	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	encoderConfig.ConsoleSeparator = " "
	encoder := zapcore.NewConsoleEncoder(encoderConfig)

	fileWriter := zapcore.AddSync(&lumberjack.Logger{
		Filename:  logPath,
		MaxSize:   logRotateSize,
		LocalTime: true,
	})
	//consoleWriter := zapcore.Lock(os.Stdout)

	core := zapcore.NewTee(
		zapcore.NewCore(encoder, fileWriter, level),
		//zapcore.NewCore(encoder, consoleWriter, level),
	)

	return zap.New(core)
}

func Debug(args ...interface{}) {
	logger.Debug(args...)
}

func Info(args ...interface{}) {
	logger.Info(args...)
}

func Warn(args ...interface{}) {
	logger.Warn(args...)
}

func Error(args ...interface{}) {
	report.ReportQiWeiLog(fmt.Sprint(args...))
	logger.Error(args...)
}

func Panic(args ...interface{}) {
	report.ReportQiWeiLog(fmt.Sprint(args...))
	logger.Panic(args...)
}

func Fatal(args ...interface{}) {
	report.ReportQiWeiLog(fmt.Sprint(args...))
	logger.Fatal(args...)
}

func Debugf(template string, args ...interface{}) {
	logger.Debugf(template, args...)
}

func Infof(template string, args ...interface{}) {
	logger.Infof(template, args...)
}

func Warnf(template string, args ...interface{}) {
	logger.Warnf(template, args...)
}

func Errorf(template string, args ...interface{}) {
	report.ReportQiWeiLog(fmt.Sprintf(template, args...))
	logger.Errorf(template, args...)
}

func Panicf(template string, args ...interface{}) {
	report.ReportQiWeiLog(fmt.Sprintf(template, args...))
	logger.Panicf(template, args...)
}

func Fatalf(template string, args ...interface{}) {
	report.ReportQiWeiLog(fmt.Sprintf(template, args...))
	logger.Fatalf(template, args...)
}

func Debugw(msg string, keysAndValues ...interface{}) {
	logger.Debugw(msg, keysAndValues...)
}

func Infow(msg string, keysAndValues ...interface{}) {
	logger.Infow(msg, keysAndValues...)
}

func Warnw(msg string, keysAndValues ...interface{}) {
	logger.Warnw(msg, keysAndValues...)
}

func Errorw(msg string, keysAndValues ...interface{}) {
	ret, err := json.Marshal(keysAndValues)
	if err == nil {
		report.ReportQiWeiLog(fmt.Sprint(msg, string(ret)))
	} else {
		log.Println("Error w marshal error~")
	}
	logger.Errorw(msg, keysAndValues...)
}

func Panicw(msg string, keysAndValues ...interface{}) {
	logger.Panicw(msg, keysAndValues...)
}

func Fatalw(msg string, keysAndValues ...interface{}) {
	logger.Fatalw(msg, keysAndValues...)
}

func Sync() {
	logger.Sync()
}
