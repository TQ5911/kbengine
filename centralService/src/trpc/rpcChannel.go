package trpc

import (
	"bytes"
	"centralService/src/appLog"
	"encoding/binary"
	"errors"
	"log"
	"net"
	"strconv"
	"time"
	"unsafe"

	"github.com/golang/protobuf/proto"
	"github.com/google/uuid"
)

func NewRpcChannel(rpcUuid uuid.UUID, conn net.Conn) *RpcChannel {
	channel := &RpcChannel{uuid.New(), conn, nil, RpcRequest{}, RpcRequestReader{}}
	channel.RpcRequestReader.reset()
	channel.RpcRequest.reset()
	return channel
}

type RpcChannel struct {
	ChannelUUID      uuid.UUID
	RawConn          net.Conn
	endPoint         IEndPoint
	RpcRequest       RpcRequest
	RpcRequestReader RpcRequestReader
}

// protobuf data stored in little endian byte order
var rpcChannelByteOrder = binary.LittleEndian

func (self *RpcChannel) getConn() net.Conn {
	return self.RawConn
}

func (self *RpcChannel) GetEndPoint() IEndPoint {
	return self.endPoint
}

func (self *RpcChannel) SetEndPoint(ep IEndPoint) {
	self.endPoint = ep
}

func (self *RpcChannel) Disconnect() {
	self.getConn().Close()
}

func (self *RpcChannel) Process() {
	defer self.Disconnect()

	service, ok := self.endPoint.(IChannelService)
	if !ok {
		return
	}
	defer service.OnLoseConnection()

	data := make([]byte, 4096)
	conn := self.RawConn
	for {
		err := conn.SetReadDeadline(time.Now().Add(10 * 2 * time.Second))
		if err != nil {
			appLog.Warnf("set read deadline failed:  %v %v\n", conn.RemoteAddr(), err)
			return
		}
		readLen, err := conn.Read(data)
		if err != nil || readLen == 0 {
			//log.Printf("connection lost: %v %v\n", conn.RemoteAddr(), err)
			return
		}

		err = self.ReadData(data[:readLen])
		if err != nil {
			return
		}
	}
}

func (self *RpcChannel) GetRemoteAddr() net.Addr {
	return self.RawConn.RemoteAddr()
}

func (self *RpcChannel) CallMethod(method *MethodDesc, msg proto.Message) error {
	msgData, err := proto.Marshal(msg)
	if err != nil {
		appLog.Error("encode proto message error:", method.MethodName, err.Error())
		return err
	}

	dataBuffer := bytes.Buffer{}
	binary.Write(&dataBuffer, rpcChannelByteOrder, method.MethodIndex)
	dataBuffer.Write(msgData)

	dataBufLen := uint32(dataBuffer.Len())
	lenSize := unsafe.Sizeof(dataBufLen)
	if lenSize != 4 {
		log.Fatalln("check message size error:", dataBufLen, lenSize)
	}

	sendBuf := bytes.Buffer{}
	binary.Write(&sendBuf, rpcChannelByteOrder, dataBufLen)
	sendBuf.Write(dataBuffer.Bytes())

	//log.Println("call remote:", method.MethodName, dataBufLen, dataBuffer.Bytes())
	nWrote, werr := self.RawConn.Write(sendBuf.Bytes())
	if werr != nil {
		appLog.Error("send data error ", method.MethodName, werr)

		service, ok := self.endPoint.(IChannelService)
		if ok {
			service.OnLoseConnection()
		}
		self.Disconnect()
	}
	if nWrote != sendBuf.Len() {
		appLog.Error("bad write:", method.MethodName)
	}

	return werr
}

func (self *RpcChannel) ReadData(dataBuf []byte) error {
	totalConsumed := 0
	dataLen := len(dataBuf)
	for totalConsumed < dataLen {
		didReadRequest, consumedLen, err := self.RpcRequestReader.readRequest(&self.RpcRequest, dataBuf, totalConsumed)
		if err != nil {
			appLog.Error("read error:", err.Error())
			return err
		}

		totalConsumed += consumedLen

		if didReadRequest {
			_, err := self.handleRequest()
			//handleRequest出错就返回错误，外层处理错误时，这个链接的goroutine也会结束，连接断开
			if err != nil {
				appLog.Error("handle request error: ", err)
				return err
			}
			self.RpcRequest.reset()
			self.RpcRequestReader.reset()
		}
	}

	return nil
}

func (self *RpcChannel) handleRequest() (interface{}, error) {
	indexBuf := [2]byte{}
	_, err := self.RpcRequest.data.Read(indexBuf[:2])
	if err != nil {
		return false, err
	}
	methodIndex := rpcChannelByteOrder.Uint16(indexBuf[:2])
	service, ok := self.endPoint.(IChannelService)
	if !ok {
		return false, errors.New("invalid service")
	}
	if int(methodIndex) >= len(service.GetServiceDesc().Methods) {
		return false, errors.New(service.GetServiceDesc().ServiceName + " invalid method index: " + strconv.Itoa(int(methodIndex)))
	}

	dec := func(v interface{}) error {
		msg, ok := v.(proto.Message)
		if !ok {
			return errors.New("require proto.Message")
		}
		err := proto.Unmarshal(self.RpcRequest.data.Bytes(), msg)
		if err != nil {
			appLog.Error("unmarshal error: ", err)
			return err
		}
		return nil
	}

	methodDesc := service.GetServiceDesc().Methods[methodIndex]
	return methodDesc.Handler(self.endPoint, dec)
}
