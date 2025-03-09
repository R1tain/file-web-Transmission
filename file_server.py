#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socketserver
import http.server
from http import HTTPStatus
import urllib.parse
import mimetypes
import cgi
import threading

# 配置参数
PORT = 55673
UPLOAD_DIR = "uploads"  # 上传目录
CHUNK_SIZE = 1024 * 1024  # 1MB 块大小，用于文件传输

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """多线程HTTP服务器"""
    daemon_threads = True

class FileHandler(http.server.BaseHTTPRequestHandler):
    """处理文件上传和下载的HTTP请求处理器"""

    def do_GET(self):
        """处理GET请求，展示文件列表或下载文件"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed_path.path)

        # 处理根路径，显示文件列表
        if path == "/":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # 获取上传目录中的文件列表
            files = os.listdir(UPLOAD_DIR)
            files.sort()

            # 构建优化的HTML响应
            html = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>文件传输服务器</title><style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap');
body{font-family:'Nunito',sans-serif;max-width:900px;margin:0 auto;padding:20px;background-color:#f8f9fa;color:#343a40;line-height:1.6}
h1{color:#2c3e50;text-align:center;margin:20px 0;font-weight:700;letter-spacing:-0.5px}
.container{background-color:#fff;border-radius:10px;padding:20px;box-shadow:0 4px 6px rgba(0,0,0,0.1)}
.file-list{list-style:none;padding:0}
.file-item{padding:12px 15px;margin:8px 0;background-color:#f8f9fa;border-left:4px solid #4361ee;border-radius:4px;display:flex;justify-content:space-between;align-items:center;transition:all 0.2s ease}
.file-item:hover{transform:translateX(5px);background-color:#f0f1f2}
.file-link{text-decoration:none;color:#4361ee;flex-grow:1;font-weight:600}.file-link:hover{color:#3046c0}
.upload-area{margin:25px 0;padding:20px;background-color:#e9ecef;border-radius:8px;text-align:center}
.file-input{margin-bottom:15px;width:100%;max-width:300px}
.btn{padding:10px 18px;background-color:#4361ee;color:white;border:none;border-radius:6px;cursor:pointer;font-weight:600;letter-spacing:0.5px;transition:all 0.2s}
.btn:hover{background-color:#3046c0;transform:translateY(-2px);box-shadow:0 4px 8px rgba(67,97,238,0.2)}
.no-files{text-align:center;color:#6c757d;margin:30px 0;font-style:italic}
.file-size{color:#6c757d;margin-left:10px;font-size:0.9em}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:15px;border-bottom:1px solid #dee2e6}
footer{text-align:center;margin-top:30px;color:#6c757d;font-size:0.9em}
</style></head><body><div class="container"><div class="header"><h1>文件传输服务器</h1></div>
<div class="upload-area">
<form action="/upload" method="post" enctype="multipart/form-data">
<input class="file-input" type="file" name="file" multiple><button class="btn" type="submit">上传文件</button>
</form></div>"""

            if files:
                html += '<ul class="file-list">'
                for filename in files:
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    if os.path.isfile(file_path):
                        file_size = self.human_readable_size(os.path.getsize(file_path))
                        html += f'<li class="file-item"><a class="file-link" href="/download/{filename}">{filename}</a><span class="file-size">{file_size}</span></li>'
                html += '</ul>'
            else:
                html += '<p class="no-files">暂无文件，请上传文件</p>'

            html += '</div><footer>© 高速文件传输服务器</footer></body></html>'

            self.wfile.write(html.encode("utf-8"))
            return

        # 处理文件下载请求
        elif path.startswith("/download/"):
            filename = os.path.basename(path[10:])
            file_path = os.path.join(UPLOAD_DIR, filename)

            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                self.send_error(HTTPStatus.NOT_FOUND, "找不到文件")
                return

            # 获取文件类型
            content_type = mimetypes.guess_type(file_path)[0]
            if not content_type:
                content_type = "application/octet-stream"

            # 设置响应头
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(os.path.getsize(file_path)))
            self.end_headers()

            # 使用分块传输文件
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(CHUNK_SIZE)
                    if not data:
                        break
                    try:
                        self.wfile.write(data)
                    except ConnectionError:
                        break
            return

        # 其他路径返回404
        self.send_error(HTTPStatus.NOT_FOUND, "资源不存在")

    def do_POST(self):
        """处理POST请求，用于文件上传"""
        if self.path == "/upload":
            try:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': self.headers['Content-Type'],
                    }
                )

                # 处理上传的文件
                if 'file' in form:
                    file_items = form['file']
                    if not isinstance(file_items, list):
                        file_items = [file_items]

                    for file_item in file_items:
                        if file_item.filename:
                            safe_filename = os.path.basename(file_item.filename)
                            file_path = os.path.join(UPLOAD_DIR, safe_filename)

                            with open(file_path, 'wb') as f:
                                f.write(file_item.file.read())

                # 重定向回首页
                self.send_response(HTTPStatus.FOUND)
                self.send_header("Location", "/")
                self.end_headers()

            except Exception as e:
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
            return

        self.send_error(HTTPStatus.NOT_FOUND, "资源不存在")

    @staticmethod
    def human_readable_size(size, decimal_places=2):
        """将字节数转换为人类可读的格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0 or unit == 'TB':
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"

def run_server():
    """运行HTTP服务器"""
    try:
        server = ThreadedHTTPServer(("", PORT), FileHandler)
        print(f"文件服务器启动在端口 {PORT}...")
        print(f"请在浏览器中打开 http://localhost:{PORT}/")
        print(f"上传目录: {os.path.abspath(UPLOAD_DIR)}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n关闭服务器...")
        server.shutdown()

if __name__ == "__main__":
    run_server()
