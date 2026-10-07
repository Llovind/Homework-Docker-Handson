from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        nim = os.getenv('STUDENT_NIM', '12345678')
        message = f"<h1>Praktikum Docker Dasar Berhasil!</h1><p>Dikembangkan oleh NIM: {nim}</p>"
        self.wfile.write(message.encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    print("Server berjalan pada port 8000...")
    server.serve_forever()