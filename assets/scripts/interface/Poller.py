# -*- coding: utf-8 -*-
import KBEngine
import socket
from KBEDebug import *


class Poller:
    """
    演示：
    可以向kbengine注册一个socket，由引擎层的网络模块处理异步通知收发。
    用法: 
    from Poller import Poller
    poller = Poller()
    
    开启(可在onBaseappReady执行)
    poller.start("localhost", 12345)
    
    停止
    poller.stop()
    """

    def __init__(self):
        self._socket = None
        self._clientsDic = {}

    def start(self, address, port):
        """
        virtual method.
        """
        self._socket = socket.socket()
        self._socket.bind((address, port))
        self._socket.listen(10)

        KBEngine.registerReadFileDescriptor(self._socket.fileno(), self.onRecvCB)

    def stop(self):
        if not self._socket:
            return

        KBEngine.deregisterReadFileDescriptor(self._socket.fileno())
        self._socket.close()
        self._socket = None

    def onRecvCB(self, fileno):
        if self._socket.fileno() == fileno:
            _sock, addr = self._socket.accept()
            self._clientsDic[_sock.fileno()] = (_sock, addr)
            KBEngine.registerReadFileDescriptor(_sock.fileno(), self.onRecvCB)
            LOG_DBG("Poller::onRecvCB: new channel[%s/%i]" % (addr, _sock.fileno()))
        else:
            _sock, addr = self._clientsDic.get(fileno, None)
            if _sock is None:
                return

            data = _sock.recv(2048)
            LOG_DBG("Poller::onRecvCB: %s/%i get data, size=%i" % (addr, _sock.fileno(), len(data)))
            self.processData(_sock, data)
            KBEngine.deregisterReadFileDescriptor(_sock.fileno())
            _sock.close()
            del self._clientsDic[fileno]

    def onWrite(self, fileno):
        pass

    def processData(self, sock, datas):
        """
        处理接收数据
        """
