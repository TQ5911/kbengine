# -*- coding: utf-8 -*-

import socket
from rpc.TcpConnection import TcpConnection
from rpc.RpcChannel import RpcChannel
from KBEDebug import *


class TcpClient(TcpConnection):

    def __init__(self, ip, port, stub_factory, rpc_service, adminStub):
        TcpConnection.__init__(self, None, (ip, port))
        self.stub_factory = stub_factory
        self.rpc_service = rpc_service
        self.channel = None
        self.stub = None
        self.adminStub = adminStub

    def afterClose(self):
        DEBUG_MSG('in TcpClient.afterClose')
        self.adminStub.gmCenterClosed()

    def sync_connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.peername)
        except socket.error as msg:
            sock.close()
            return False

        # after connected, do the nonblocking setting
        sock.setblocking(0)
        self.set_socket(sock)
        self.setsockopt()
        self.handle_connect()
        return True

    def handle_connect(self):
        self.status = TcpConnection.ST_ESTABLISHED
        #service是被动接收方，stub是主动发送方
        self.channel = RpcChannel(self.rpc_service, self)
        self.stub = self.stub_factory(self.channel)
        self.attach_rpc_channel(self.channel)

    def handle_close(self):
        DEBUG_MSG('Attention!!! TcpClient.handle_close')
        super().handle_close()
        self.afterClose()

    def handle_expt(self):
        DEBUG_MSG('Attention!!! TcpClient.handle_expt')
        super().handle_expt()
        self.afterClose()

    def handle_error(self):
        DEBUG_MSG('Attention!!! TcpClient.handle_error')
        super().handle_expt()
        self.afterClose()

    def writable(self):
        if self.status == TcpConnection.ST_ESTABLISHED:
            return TcpConnection.writable(self)
        else:
            return True
