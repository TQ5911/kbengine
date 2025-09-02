# -*- coding: utf-8 -*-
import asyncore
import socket
import KBEDebug


class SocketClient(asyncore.dispatcher):

    def __init__(self, host):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.doConnect()
        self.buffer = b''

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()
        self.buffer = b''

    def handle_expt(self):
        self.close()
        self.buffer = b''

    def handle_read(self):
        print(self.recv(8192))

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def doConnect(self):
        try:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect(self.host)
        except Exception as e:
            self.close()
            self.doConnect()


class UdpSocketClient(asyncore.dispatcher):

    def __init__(self, remoteAddr):
        asyncore.dispatcher.__init__(self)
        self.remoteAddr = remoteAddr
        self.pendingPacket = []
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.debug = True

    def sendto(self, packet):
        self.pendingPacket.append(packet)

    def writeable(self):
        return len(self.pendingPacket) > 0

    def handle_write(self):
        if len(self.pendingPacket) > 0:
            p = self.pendingPacket.pop(0)
            print('MapleDirClient handle_write ', p)
            self.socket.sendto(p, self.remoteAddr)

    def handle_read(self):
        data = self.recv(8192)
        self.recvResult(data)

    def recvResult(self, data):
        pass

    def handle_close(self):
        self.close()

    def handle_connect(self):
        pass
