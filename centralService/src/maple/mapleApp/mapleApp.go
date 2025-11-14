package MapleApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/trpc"
	"database/sql"
	"fmt"
	"net"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

type MapleApp struct {
	common.App
	mapleHttpService *MapleHttpService
	db               *sql.DB
}

func NewMapleApp() *MapleApp {
	mysqlUrl := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		MapleConfig.Mysql.User, MapleConfig.Mysql.Passwd, MapleConfig.Mysql.Addr, MapleConfig.Mysql.Db)
	db, err := sql.Open("mysql", mysqlUrl)
	if err != nil {
		appLog.Error("open db error: ", err.Error())
		return nil
	}

	db.SetMaxIdleConns(50)
	db.SetConnMaxLifetime(time.Second * 290)
	db.SetMaxOpenConns(50)
	if err = db.Ping(); err != nil {
		appLog.Error("mysql connect err", err.Error())
		return nil
	}

	ma := MapleApp{
		db: db,
	}

	return &ma
}

func (ma *MapleApp) Start() {
	appLog.Info("start maple app ma is ", ma)
	ma.mapleHttpService = NewMapleHttpService(ma)
	ma.mapleHttpService.start(MapleConfig.HttpAddr)
}

func (ma *MapleApp) GetName() string {
	return ""
}

func (ma *MapleApp) GetServices() []*common.ServiceInfo {
	return nil
}

func (ma *MapleApp) NewService(net.Conn, uint8) trpc.IServerEndPoint {
	return nil
}
