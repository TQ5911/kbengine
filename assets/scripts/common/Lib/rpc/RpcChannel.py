# -*- coding: UTF-8 -*-
#rpc channel for external tool service
from google.protobuf import service
from . import RpcDispatcher
from . import RpcRequest
import socket
from struct import pack, unpack

REPORT_ERR_FUNC = None

class RpcSyncChannel(service.RpcChannel):

    def __init__(self, service_interface_obj, connected_socket=None):
        super(RpcSyncChannel, self).__init__()
        self.service_interface_obj = service_interface_obj
        self.rpc_request = RpcRequest.request()
        self.rpc_request_parser = RpcRequest.request_parser()
        self.buffer_size = 16384

        if connected_socket:
            self._socket = connected_socket
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sync_on = True

    def sync_mode(self, on):
        self.sync_on = on

    def set_buffer(self, size):
        self.buffer_size = size

    def set_socket_buffer(self, recv_buffer_size, send_buffer_size):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buffer_size)

    def set_max_data(self, size):
        self.rpc_request_parser.set_max_data(size)

    def connect(self, address):
        self._socket.connect(address)

    def disconnect(self):
        self._socket.close()
        self._socket = None
        self.rpc_request.reset()
        self.rpc_request_parser.reset()

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        cmd_index = method_descriptor.index
        assert(cmd_index < 65535)

        data = request.SerializeToString()
        total_len = len(data) + 2

        try:
            self._socket.send(pack('<I', total_len))
            self._socket.send(pack('<H', cmd_index))
            self._socket.send(data)

            if self.sync_on:
                self.fetch_result()
        except:
            self.disconnect()
            self.service_interface_obj.on_disconnected()
            raise

    def input_data(self, data):
        total = len(data)
        skip = 0
        while skip < total:
            result, consum = self.rpc_request_parser.parse(self.rpc_request, data, skip)
            assert(consum > 0)

            skip += consum
            # true, already got a complete request
            if result == 1:
                ok = self.on_request()

                self.rpc_request.reset()
                # disconnect if not ok
                if not ok:
                    return 0

                if skip == total:
                    return 1

                continue
            # false, bad request, need to disconnect
            elif result == 0:
                return 0

            # need more data
            else:
                continue
        # need more data
        return 2

    def on_request(self):
        l = len(self.rpc_request.data)

        # sizeof(cmd_index) == 2
        if l < 2:
            print('Got error request size: ', l)
            return False

        index_data = self.rpc_request.data[0:2]

        cmd_index = unpack('<H', index_data)[0]

        s_descriptor = self.service_interface_obj.GetDescriptor()

        if cmd_index > len(s_descriptor.methods):
            print('Got error method index:', cmd_index)
            return False

        method = s_descriptor.methods[cmd_index]

        request = self.service_interface_obj.GetRequestClass(method)()

        serialized = self.rpc_request.data[2:]

        request.ParseFromString(serialized)

        self.service_interface_obj.CallMethod(method, None, request, None)

        return True

    def fetch_result(self):
        while 1:
            data = self._socket.recv(self.buffer_size)
            #print('fetch_result', len(data), repr(data)

            if data:
                rc = self.input_data(data)

                if rc == 2:
                    continue
                elif rc == 0:
                    # error, then close
                    self.disconnect()
                    return
                else:
                    # == 1
                    break

class RpcChannel(service.RpcChannel):

    def __init__(self, service_interface_obj, accept_connection=None):
        super(RpcChannel, self).__init__()
        self.service_interface_obj = service_interface_obj
        self.rpc_request = RpcRequest.request()
        self.rpc_request_parser = RpcRequest.request_parser()
        if accept_connection:
            self.dispatcher = RpcDispatcher.dispatcher(self, accept_connection=accept_connection)
        else:
            self.dispatcher = None

        self.recv_buffer_size = 0
        self.recv_socket_buffer_size = 0
        self.send_socket_buffer_size = 0

    def set_service_interface_obj(self, obj):
        self.service_interface_obj = obj

    def set_buffer(self, size):
        self.recv_buffer_size = size
        if self.dispatcher:
            self.dispatcher.set_buffer(size)

    def set_socket_buffer(self, recv_buffer_size, send_buffer_size):
        self.recv_socket_buffer_size = recv_buffer_size
        self.send_socket_buffer_size = send_buffer_size

        if self.dispatcher:
            self.dispatcher.set_socket_buffer(recv_buffer_size, send_buffer_size)

    def set_max_data(self, size):
        self.rpc_request_parser.set_max_data(size)

    def connect(self, address):
        self.dispatcher = RpcDispatcher.dispatcher(self)
        try:
            self.dispatcher.connect(address)
        except Exception as e:
            print('fail to connect', repr(e))

        if self.recv_buffer_size:
            self.dispatcher.set_buffer(self.recv_buffer_size)

        if self.recv_socket_buffer_size > 0 and self.send_socket_buffer_size > 0:
            self.dispatcher.set_socket_buffer(self.recv_socket_buffer_size, self.send_socket_buffer_size)

    def on_connected(self):
        print('RpcChannel.on_connected')

        if self.service_interface_obj:
            self.service_interface_obj.on_connected()

    def on_disconnected(self):
        print('RpcChannel.on_disconnected')
        if self.service_interface_obj:
            self.service_interface_obj.on_disconnected()

        self.dispatcher = None
        self.rpc_request.reset()
        self.rpc_request_parser.reset()

    def disconnect(self):
        self.dispatcher.disconnect()
        self.dispatcher = None
        self.rpc_request.reset()
        self.rpc_request_parser.reset()


    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        cmd_index = method_descriptor.index
        assert(cmd_index < 65535)

        data = request.SerializeToString()
        newReq = type(request)()
        newReq.ParseFromString(data)
        total_len = len(data) + 2

        if not self.dispatcher:
            if REPORT_ERR_FUNC:
                REPORT_ERR_FUNC('connection lost, call remote method err:', method_descriptor.full_name)
            return

        self.dispatcher.send_data(pack('<I', total_len))
        self.dispatcher.send_data(pack('<H', cmd_index))
        self.dispatcher.send_data(data)

#		if done:
#			done()
    def input_data(self, data):
        total = len(data)
        skip = 0
        while skip < total:
            result, consum = self.rpc_request_parser.parse(self.rpc_request, data, skip)
            assert(consum > 0)

            skip += consum
            # true, already got a complete request
            if result == 1:
                ok = self.on_request()

                self.rpc_request.reset()
                # disconnect if not ok
                if not ok:
                    return 0

                continue

            # false, bad request, need to disconnect
            elif result == 0:
                return 0

            # need more data
            else:
                continue
        # need more data
        return 2

    def on_request(self):

        l = len(self.rpc_request.data)

        # sizeof(cmd_index) == 2
        if l < 2:
            print('Got error request size: ', l)
            return False

        index_data = self.rpc_request.data[0:2]

        cmd_index = unpack('<H', index_data)[0]

        s_descriptor = self.service_interface_obj.GetDescriptor()

        if cmd_index > len(s_descriptor.methods):
            print('Got error method index:', cmd_index)
            return False

        method = s_descriptor.methods[cmd_index]

        request = self.service_interface_obj.GetRequestClass(method)()

        serialized = self.rpc_request.data[2:]

        request.ParseFromString(serialized)
        try:
            self.service_interface_obj.CallMethod(method, None, request, None)
        except Exception as e:
            if REPORT_ERR_FUNC:
                REPORT_ERR_FUNC('call local method err:', method.full_name, e)
            else:
                print('call method err:', method.full_name)

        return True


class SSLRpcChannel(RpcChannel):

    def __init__(self, certfile, service_interface_obj):
        super(SSLRpcChannel, self).__init__(service_interface_obj)
        self.certfile = certfile

    def connect(self, address):
        self.dispatcher = RpcDispatcher.dispatcher_ssl(self.certfile, self)
        self.dispatcher.connect(address)


    def on_handshaked(self):
        print('SSLRpcChannelSSL.on_handshaked')

        if self.service_interface_obj:
            self.service_interface_obj.on_handshaked()
