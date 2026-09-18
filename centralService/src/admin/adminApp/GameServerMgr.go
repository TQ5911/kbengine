package adminApp

import (
	"bytes"
	"centralService/src/appLog"
	"centralService/src/common"
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"sync"
	"time"
)

const (
	UNKNOWN_COMPONENT_TYPE = 0
	DBMGR_TYPE             = 1
	LOGINAPP_TYPE          = 2
	BASEAPPMGR_TYPE        = 3
	CELLAPPMGR_TYPE        = 4
	CELLAPP_TYPE           = 5
	BASEAPP_TYPE           = 6
	CLIENT_TYPE            = 7
	MACHINE_TYPE           = 8
	CONSOLE_TYPE           = 9
	LOGGER_TYPE            = 10
	BOTS_TYPE              = 11
	WATCHER_TYPE           = 12
	INTERFACES_TYPE        = 13
	TOOL_TYPE              = 14
	COMPONENT_END_TYPE     = 15
)

type CompVal struct {
	uid         uint32
	compType    CompType
	componentId uint64
	groupOrder  uint32
	intAddr     uint32
	intPort     uint16
	conn        net.Conn
}

func (self *CompVal) getIntConn() net.Conn {
	if self.conn != nil {
		return self.conn
	}

	intAddr := fmt.Sprintf("%s:%d", common.InetNtoA(self.intAddr), self.intPort)
	appLog.Debug("connect to component:", intAddr)
	conn, err := net.DialTimeout("tcp", intAddr, time.Second*2)
	if err != nil {
		appLog.Error("fail to connect to game server internal interface:", intAddr, self.intPort)
		return nil
	}

	self.conn = conn

	self.startActiveTick()
	return self.conn
}

func (self *CompVal) startActiveTick() {
	timer := time.NewTimer(10 * time.Second)
	go func(t *time.Timer) {
		for {
			<-t.C
			sendBuf := bytes.Buffer{}

			var appMsgId uint16 = 0
			var myCompType CompType = CONSOLE_TYPE
			var myCompId uint64 = 1

			switch self.compType {
			case CELLAPP_TYPE:
				appMsgId = 55101
				break
			case BASEAPP_TYPE:
				appMsgId = 55100
				break
			case BOTS_TYPE:
				appMsgId = 55107
				break
			default:
				appLog.Error("unsupported component type!", self.compType)
				return
			}

			binary.Write(&sendBuf, byteOrder, appMsgId)
			binary.Write(&sendBuf, byteOrder, myCompType)
			binary.Write(&sendBuf, byteOrder, myCompId)

			sendBytes := sendBuf.Bytes()
			_, err := self.conn.Write(sendBytes)
			if err != nil {
				appLog.Error("tick error", err)
				self.reconnectToGameServer()
				return
			} else {
				t.Reset(10 * time.Second)
			}
		}
	}(timer)
}

func (self *CompVal) reconnectToGameServer() net.Conn {
	appLog.Debug("reconnect")
	self.conn.Close()
	self.conn = nil
	return self.getIntConn()
}

type ServerId uint32
type CompType uint32
type ComponentList []*CompVal
type Components map[CompType]ComponentList
type ServerComponents map[ServerId]*Components

func (comps Components) reset() {
	for _, compList := range comps {
		for _, comp := range compList {
			conn := comp.conn
			if conn != nil {
				conn.Close()
			}
		}
	}
}

var byteOrder = binary.LittleEndian

func findComponents(ip string) *Components {
	allComps := make(Components)

	var uid uint32 = 1
	var myCompType CompType = CONSOLE_TYPE
	var myCompId uint64 = 1
	var receiveIpAddr uint32 = 0
	var receivePort uint16 = 0
	var findInterfaceMsgId uint16 = 1
	var terminateChar uint8 = 0

	findTypes := []CompType{CELLAPP_TYPE, BASEAPP_TYPE, BOTS_TYPE}
	group := sync.WaitGroup{}
	compsMapLock := sync.Mutex{}

	for _, findCompType := range findTypes {
		group.Add(1)
		compList := make(ComponentList, 0, 10)
		allComps[findCompType] = compList
		go func(compType CompType) {
			defer group.Done()

			conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, adminConfig.MachinePort), time.Second*3)
			if err != nil {
				appLog.Warn("fail to connect machine:", ip)
				return
			}

			defer conn.Close()

			sendBuf := bytes.Buffer{}
			var msgLen uint16 = 0

			binary.Write(&sendBuf, byteOrder, findInterfaceMsgId)
			binary.Write(&sendBuf, byteOrder, msgLen)
			binary.Write(&sendBuf, byteOrder, uid)
			sendBuf.WriteString("gmt")
			binary.Write(&sendBuf, byteOrder, terminateChar)
			binary.Write(&sendBuf, byteOrder, myCompType)
			binary.Write(&sendBuf, byteOrder, myCompId)
			binary.Write(&sendBuf, byteOrder, compType)
			binary.Write(&sendBuf, byteOrder, receiveIpAddr)
			binary.Write(&sendBuf, byteOrder, receivePort)

			msgLen = uint16(sendBuf.Len()) - 4
			msgLenBytes := make([]byte, 2, 2)
			sendBytes := sendBuf.Bytes()
			binary.LittleEndian.PutUint16(msgLenBytes, msgLen)
			copy(sendBytes[2:4], msgLenBytes[:])

			n, err := conn.Write(sendBuf.Bytes())
			if err != nil {
				appLog.Error("find components failed:", err.Error(), n)
				return
			}

			readBuf := bytes.NewBuffer(make([]byte, 0, 65535))
			data := make([]byte, 1024)
			for {
				conn.SetReadDeadline(time.Now().Add(5 * time.Second))
				readLen, err := conn.Read(data)
				if err != nil {
					break
				}
				readBuf.Write(data[:readLen])
			}

			var compUid uint32 = 0
			var targetCompType CompType = 0
			var compId uint64 = 0
			var compIdEx uint64 = 0
			var globalOrder uint32 = 0
			var groupOrder uint32 = 0
			var gus uint32 = 0
			var intAddr uint32 = 0
			var intPort uint16 = 0
			var extAddr uint32 = 0
			var extPort uint16 = 0
			var pid uint32 = 0
			var cpu float32 = 0
			var mem float32 = 0
			var usedmem uint32 = 0
			var state uint8 = 0
			var machineID uint32 = 0
			var extraData, extraData1, extraData2, extraData3 uint64 = 0, 0, 0, 0
			var backRecvAddr uint32 = 0
			var backRevPort uint16 = 0

			for readBuf.Len() > 0 {
				binary.Read(readBuf, byteOrder, &compUid)
				username, _ := readBuf.ReadString(0)
				binary.Read(readBuf, byteOrder, &targetCompType)
				binary.Read(readBuf, byteOrder, &compId)
				binary.Read(readBuf, byteOrder, &compIdEx)
				binary.Read(readBuf, byteOrder, &globalOrder)
				binary.Read(readBuf, byteOrder, &groupOrder)
				binary.Read(readBuf, byteOrder, &gus)
				binary.Read(readBuf, binary.BigEndian, &intAddr)
				binary.Read(readBuf, binary.BigEndian, &intPort)
				binary.Read(readBuf, binary.BigEndian, &extAddr)
				binary.Read(readBuf, binary.BigEndian, &extPort)
				_, err = readBuf.ReadString(0) //extAddr
				binary.Read(readBuf, byteOrder, &pid)
				binary.Read(readBuf, byteOrder, &cpu)
				binary.Read(readBuf, byteOrder, &mem)
				binary.Read(readBuf, byteOrder, &usedmem)
				binary.Read(readBuf, byteOrder, &state)
				binary.Read(readBuf, byteOrder, &machineID)
				binary.Read(readBuf, byteOrder, &extraData)
				binary.Read(readBuf, byteOrder, &extraData1)
				binary.Read(readBuf, byteOrder, &extraData2)
				binary.Read(readBuf, byteOrder, &extraData3)
				binary.Read(readBuf, binary.BigEndian, &backRecvAddr)
				binary.Read(readBuf, binary.BigEndian, &backRevPort)

				if targetCompType != UNKNOWN_COMPONENT_TYPE {
					compsMapLock.Lock()
					allComps[compType] = append(allComps[compType], &CompVal{compUid, compType, compId, groupOrder, intAddr, intPort, nil})
					appLog.Debug("found component:", ip, compType, compUid, username, compId, groupOrder, intAddr, intPort, extAddr, extPort)
					compsMapLock.Unlock()
				}
			}

		}(findCompType)
	}

	group.Wait()

	return &allComps
}

func runScript(comp *CompVal, script string) string {
	sendBuf := bytes.Buffer{}

	var runscriptMsgId uint16 = 0
	var msgLen uint16 = 0
	//var terminateChar byte = 0
	var scriptLen uint32 = uint32(len(script))

	switch comp.compType {
	case CELLAPP_TYPE:
		runscriptMsgId = 55002
		break
	case BASEAPP_TYPE:
		runscriptMsgId = 55001
		break
	case BOTS_TYPE:
		runscriptMsgId = 55003
		break
	default:
		appLog.Error("unsupported component type!", comp.compType)
		return ""
	}

	binary.Write(&sendBuf, byteOrder, runscriptMsgId)
	binary.Write(&sendBuf, byteOrder, msgLen)
	binary.Write(&sendBuf, byteOrder, scriptLen)
	sendBuf.WriteString(script)
	//binary.Write(&sendBuf, byteOrder, terminateChar)

	msgLen = uint16(sendBuf.Len()) - 4
	msgLenBytes := make([]byte, 2, 2)
	sendBytes := sendBuf.Bytes()
	binary.LittleEndian.PutUint16(msgLenBytes, msgLen)
	copy(sendBytes[2:4], msgLenBytes[:])

RETRY_SEND:
	conn := comp.getIntConn()
	if conn == nil {
		return ""
	}
	restLen := len(sendBytes)

	for restLen > 0 {
		sentLen, err := conn.Write(sendBytes)
		restLen -= sentLen
		if err != nil {
			comp.reconnectToGameServer()
			goto RETRY_SEND
		}
	}

	readBuf := bytes.NewBuffer(make([]byte, 0, 65535))
	data := make([]byte, 1024)

	conn.SetReadDeadline(time.Now().Add(5 * time.Second))
	readLen, err := conn.Read(data)
	if err != nil {
		if err, ok := err.(net.Error); ok && err.Timeout() {

		} else {
			appLog.Error("read script result err:", err)
			comp.reconnectToGameServer()
		}

		return ""
	}
	readBuf.Write(data[:readLen])

	var callbackMsgId uint16 = 0
	var resultLen uint32 = 0

	binary.Read(readBuf, byteOrder, &callbackMsgId)
	binary.Read(readBuf, byteOrder, &msgLen)
	binary.Read(readBuf, byteOrder, &resultLen)

	resultBytes := make([]byte, resultLen)
	io.ReadFull(readBuf, resultBytes)
	result := string(resultBytes)

	if err != nil {
		appLog.Error("read script result1 err:", err)
		return ""
	}

	return result
}
