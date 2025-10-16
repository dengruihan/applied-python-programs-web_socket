from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

class myflask:
    def __init__(self, host="0.0.0.0", port=8000):

        """
        初始化Flask应用
        :param host: 服务器主机地址，默认为"0.0.0.0"
        :param port: 服务器端口号，默认为8000
        """
        self.host = host  # 服务器主机地址
        self.port = port
        self.routes = {}  # {path: {method: function}}
    
    def route(self, path, methods=["GET"]):
        def decorator(func):
            if path not in self.routes:
                self.routes[path] = {}
            for method in methods:
                self.routes[path][method] = func
            return func
        return decorator
    
    def run(self):
        class RequestHandler(BaseHTTPRequestHandler):
            flask_app = self
            
            def do_GET(self):
                self.handle_request("GET")
            
            def do_POST(self):
                self.handle_request("POST")
            
            def handle_request(self, method):
                path = self.path
                if '?' in path:
                    path = path.split('?')[0]
                
                if path in self.flask_app.routes and method in self.flask_app.routes[path]:
                    try:
                        response = self.flask_app.routes[path][method]()  # 执行路由处理函数并获取响应结果
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(response.encode('utf-8'))
                    except Exception as e:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write("404 Not Found".encode('utf-8'))
            
            def log_message(self, format, *args):
                pass  # 静默日志输出
        
        server = HTTPServer((self.host, self.port), RequestHandler)
        print(f"Server running on http://{self.host}:{self.port}")
        server.serve_forever()
