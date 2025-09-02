# -*- coding: utf-8 -*-

import socket
import asyncore

from rpc.TcpConnection import TcpConnection
from rpc.RpcChannel import RpcChannel


class TcpServer(asyncore.dispatcher):
    '''负责accept链接，并建立一条TcpConnection通道'''
    def __init__(self, ip, port, rpc_service, connMgr):
        asyncore.dispatcher.__init__(self)
        self.ip = ip
        self.port = port
        self.rpc_service = rpc_service
        self.connMgr = connMgr

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((self.ip, self.port))
        self.listen(50)

    def handle_accept(self):
        try:
            sock, addr = self.accept()
        except socket.error as e:
            return
        except TypeError as e:
            return

        conn = TcpConnection(sock, addr)
        rpc_channel = RpcChannel(self.rpc_service, sock)
        conn.attach_rpc_channel(rpc_channel)
        self.connMgr.handleNewConnection(conn)

    def stop(self):
        self.close()



