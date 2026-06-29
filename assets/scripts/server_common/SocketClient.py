# -*- coding: utf-8 -*-
import asyncore
import socket


class SocketClient(asyncore.dispatcher):

    def __init__(self, host, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.doConnect()
        self.buffer = bytes()

    def handle_close(self):
        self.close()
        self.buffer = bytes()

    def handle_connect(self):
        pass

    def handle_expt(self):
        self.close()
        self.buffer = b''

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_read(self):
        print(self.recv(8192))

    def doConnect(self):
        try:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect(self.host)
        except Exception as _:
            self.close()
            self.doConnect()

    def handle_write(self):
        _sent = self.send(self.buffer)
        self.buffer = self.buffer[_sent:]


class UdpSocketClient(asyncore.dispatcher):

    def __init__(self, remoteAddr, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.pendingPacket = []
        self.remoteAddr = remoteAddr
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.debug = True

    def writeable(self):
        return len(self.pendingPacket) > 0

    def sendto(self, packet):
        self.pendingPacket.append(packet)

    def handle_write(self):
        if len(self.pendingPacket) > 0:
            _p = self.pendingPacket.pop(0)
            print('MapleDirClient handle_write ', _p)
            self.socket.sendto(_p, self.remoteAddr)

    def handle_read(self):
        data = self.recv(8192)
        self.recvResult(data)

    def handle_close(self):
        self.close()

    def recvResult(self, data):
        pass

    def handle_connect(self):
        pass
