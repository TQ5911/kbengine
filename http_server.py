# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time

# # 自定义请求处理器，处理不同资源的访问逻辑
# class CustomRequestHandler(BaseHTTPRequestHandler):
#     # 处理 GET 请求
#     def do_GET(self):
#         # 1. 访问 "/A" 资源：立即返回成功响应
#         if self.path == "/A":
#             self.send_response(200)  # 状态码：200 OK
#             self.send_header("Content-Type", "text/plain; charset=utf-8")
#             self.end_headers()
#             # 向客户端返回内容
#             response_content = "访问资源 A 成功！（立即返回）".encode("utf-8")
#             self.wfile.write(response_content)
        
#         # 2. 访问 "/B" 资源：延迟 10 秒后返回
#         elif self.path == "/B":
#             # 关键：延迟 10 秒（模拟服务处理耗时）
#             time.sleep(10)
#             # 延迟结束后返回响应
#             self.send_response(200)  # 状态码：200 OK
#             self.send_header("Content-Type", "text/plain; charset=utf-8")
#             self.end_headers()
#             response_content = "访问资源 B 成功！（延迟 10 秒后返回）".encode("utf-8")
#             self.wfile.write(response_content)
        
#         # 3. 访问其他不存在的资源：返回 404 错误
#         else:
#             self.send_response(404)  # 状态码：404 Not Found
#             self.send_header("Content-Type", "text/plain; charset=utf-8")
#             self.end_headers()
#             response_content = "资源不存在！请访问 /A 或 /B".encode("utf-8")
#             self.wfile.write(response_content)

# # 启动服务器的函数
# def run_server(host="localhost", port=23456):
#     server_address = (host, port)
#     # 创建 HTTP 服务器实例，绑定处理器
#     httpd = HTTPServer(server_address, CustomRequestHandler)
#     print(f"服务器已启动！地址：http://{host}:{port}")
#     print(f"可访问的资源：")
#     print(f"- 立即返回：http://{host}:{port}/A")
#     print(f"- 延迟 10 秒返回：http://{host}:{port}/B")
#     print("按下 Ctrl+C 可停止服务器")
    
#     try:
#         # 持续监听请求（无限循环）
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         # 捕获 Ctrl+C 信号，优雅停止服务器
#         httpd.server_close()
#         print("\n服务器已停止")

# # 程序入口
# if __name__ == "__main__":
#     # 默认在本地 23456 端口启动，可根据需要修改 host 和 port
#     run_server(host="localhost", port=23456)


from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("do_GET ", self.path)
        if self.path == '/A':
            # 模拟10秒延迟
            time.sleep(5)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"GET Response from /A dealay")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"GET Response from other")

    def do_POST(self):
        print("do_POST ", self.path)

        # 1. 获取body长度
        content_len = int(self.headers.get('Content-Length', 0))
        # 2. 读取原始二进制body
        raw_body = self.rfile.read(content_len)
        # 转utf8字符串
        body_str = raw_body.decode("utf-8")
        print("原始body字符串:", content_len, body_str)

        # 3. 根据Content-Type解析参数
        content_type = self.headers.get("Content-Type", "")
        post_data = {}

        if "application/json" in content_type:
            # JSON格式 body: {"userGameId":123}
            post_data = json.loads(body_str)
            print("解析JSON参数:", post_data)
        elif "application/x-www-form-urlencoded" in content_type:
            # 表单格式 body: userGameId=123&name=test
            parsed = parse_qs(body_str)
            # parse_qs默认值是列表，转成单值
            post_data = {k: v[0] for k, v in parsed.items()}
            print("解析表单参数:", post_data)

        if self.path == '/A':
            try:
                # 模拟10秒延迟
                time.sleep(10)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"POST Response from /A dealay")
            except BrokenPipeError:
                print("client alerady disconnected")
        elif self.path == '/B':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{\"code\":200, \"message\":\"POST Response from other\"}")

        elif self.path == '/SendCode':
            code = 200
            context = json.dumps({"code": code, "message": "alerady send"})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(context.encode("utf-8"))

        elif self.path == '/VerifyCode':
            code = 200
            msg = "verify success"
            if post_data['code'] != '123456':
                code = 1000
                msg = "verify failed"
            context = json.dumps({"code": code, "message": msg})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(context.encode("utf-8"))

def run_server():
    server_address = ('', 23456)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on port 23456...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()