import socket
from urllib.parse import urlparse, parse_qs
from html import escape

count = 0

class Request:
    def __init__(self, raw_path, method, headers, body):
        self.method = method
        self.headers = headers
        self.body = body
        url = urlparse(raw_path)
        self.path = url.path
        self.args = {k: v[0] for k, v in parse_qs(url.query).items()}




with socket.socket() as s:
    host = "0.0.0.0"
    port = 8082
    s.bind((host, port))
    s.listen(5)
    
    while True:
        count += 1
        print(f"第{count}次请求")
        conn, addr = s.accept()
        print('连接地址：', addr)
        with conn:
            data = conn.recv(4096).decode("utf-8", errors="ignore")
            
            # 解析请求
            request_line, headers_rest = data.split("\r\n", 1)
            method, path, _ = request_line.split(" ", 2)
            headers, _, body = headers_rest.partition("\r\n\r\n")
            
            # 构建 Request 对象
            req = Request(path, method, headers, body)
            
            # 使用解析后的信息构建响应
            response_body = f"<h1>Hello</h1><p>Method={req.method}</p><p>Path={req.path}</p><p>Args={req.args}</p>"
            resp = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(response_body.encode())}\r\n"
                "Connection: close\r\n\r\n"
                f"{response_body}"
            )
            conn.sendall(resp.encode('utf-8'))

