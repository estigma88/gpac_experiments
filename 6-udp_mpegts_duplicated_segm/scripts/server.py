from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import os
import sys

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    def do_PUT(self):
        path = self.path  # Retrieve the HTTP path
        last_part = os.path.basename(path)
        file_path = f"/tmp/workdir/content/{last_part}"

        sys.stderr.write(f'Received PUT request for path: {path}\n')

        with open(file_path, 'wb') as file:
            chunk_size = 4096
            while True:
                chunk = self.rfile.read(chunk_size)
                if not chunk:
                    break
                file.write(chunk)

        self.send_response(200)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server():
    host = '0.0.0.0'
    port = 8080

    os.mkdir("/tmp/workdir/content/")

    server = ThreadedHTTPServer((host, port), MyRequestHandler)
    sys.stderr.write(f'Server running on {host}:{port}\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    sys.stderr.write('Server stopped.\n')

if __name__ == '__main__':
    run_server()
