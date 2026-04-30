# -*- coding: utf-8 -*-

import socket
import asyncore
from KBEDebug import *


class TcpConnection(asyncore.dispatcher):
    """
    TcpConnection， 对应一条建立好的连接，可能来自TcpServer的accept，也可能来自TcpClient的connect
    """
    DEFAULT_RECV_BUFFER = 16384
    ST_INIT = 0
    ST_ESTABLISHED = 1
    ST_DISCONNECTED = 2

    def __init__(self, sock, peername):
        asyncore.dispatcher.__init__(self, sock)
        self.status = TcpConnection.ST_INIT
        self.peername = peername

        self.writebuff = b''
        self.recv_buff_size = TcpConnection.DEFAULT_RECV_BUFFER

        if sock:
            self.status = TcpConnection.ST_ESTABLISHED
            self.setsockopt()
        self.rpc_channel = None

    def setsockopt(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    def get_rpc_channel(self):
        return self.rpc_channel

    def set_channel_interface_obj(self, obj):
        self.rpc_channel.set_service_interface_obj(obj)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, stat):
        self._status = stat

    def attach_rpc_channel(self, channel_interface):
        self.rpc_channel = channel_interface

    def is_established(self):
        return self.status == TcpConnection.ST_ESTABLISHED

    def set_recv_buffer(self, size):
        self.recv_buff_size = size

    def disconnect(self):
        if self.status == TcpConnection.ST_DISCONNECTED:
            return

        if self.rpc_channel:
            self.rpc_channel.on_disconnected()
        self.rpc_channel = None

        if self.socket:
            asyncore.dispatcher.close(self)
        self.status = TcpConnection.ST_DISCONNECTED

    def getpeername(self):
        return self.peername

    def handle_close(self):
        LOG_DBG('Attention!!! TcpConnection.handle_close')
        asyncore.dispatcher.handle_close(self)
        self.disconnect()

    def handle_expt(self):
        LOG_DBG('Attention!!! TcpConnection.handle_expt')
        asyncore.dispatcher.handle_expt(self)
        self.disconnect()

    def handle_error(self):
        LOG_DBG('Attention!!! TcpConnection.handle_error')
        asyncore.dispatcher.handle_error(self)
        self.disconnect()

    def handle_read(self):
        data = self.recv(self.recv_buff_size)
        if data:
            if not self.rpc_channel:
                return
            self.rpc_channel.input_data(data)

    def handle_write(self):
        if self.writebuff:
            size = self.send(self.writebuff)
            self.writebuff = self.writebuff[size:]

    def writable(self):
        return len(self.writebuff) > 0

    def send_data(self, data):
        self.writebuff += data