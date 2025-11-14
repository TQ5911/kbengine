package trpc

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"log"
	"strconv"
)

const (
	_ = iota
	STATE_SIZE
	STATE_DATA
)

const DATA_LENGTH_SIZE = 4

type RpcRequest struct {
	dataSizeBuf bytes.Buffer
	data bytes.Buffer
}

func (self *RpcRequest) reset(){
	self.dataSizeBuf.Reset()
	self.data.Reset()
}

func (self *RpcRequest) getSize() int{
	return int(binary.LittleEndian.Uint32(self.dataSizeBuf.Bytes()))
}

type RpcRequestReader struct {
	state uint8
	needSize int
	rpcChannel *RpcChannel
}

func (self *RpcRequestReader) reset(){
	self.state = STATE_SIZE
	self.needSize = DATA_LENGTH_SIZE
}

func (self *RpcRequestReader) readRequest(request *RpcRequest, rawData []byte, offset int) (bool, int, error) {
	data := rawData[offset:]
	dataLen := len(data)
	if dataLen<=0{
		return false, 0, nil
	}
	switch self.state {
	case STATE_SIZE:
		if self.needSize>dataLen {
			request.dataSizeBuf.Write(data)
			self.needSize -= dataLen
			return false, dataLen, nil
		} else {
			request.dataSizeBuf.Write(data[:self.needSize])
			self.state = STATE_DATA
			consumedLen := self.needSize
			self.needSize = request.getSize()
			if self.needSize>1200*1024{
				return false, consumedLen, errors.New(fmt.Sprintf("too much data to read: %s", strconv.Itoa(self.needSize)))
			}
			return false, consumedLen, nil
		}
	case STATE_DATA:
		if self.needSize>dataLen{
			request.data.Write(data)
			self.needSize -= dataLen
			return false, dataLen, nil
		}else {
			request.data.Write(data[:self.needSize])
			consumedLen := self.needSize
			return true, consumedLen, nil
		}
	}
	log.Fatal("RpcRequestReader: bad state ", self.state)
	return false, 0, nil
}