from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json

HOST = "0.0.0.0"
PORT = 5000

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        data = json.loads(body)

        print("[🔥] Trigger received:", data)

        subprocess.run([
            "python",
            "D:\\Cyber_security\\projects\\main.py",
            "--trigger-source", data.get("agent"),
            "--incident-type", data.get("description"),
            "--severity", str(data.get("level"))
        ])

        self.send_response(200)
        self.end_headers()

server = HTTPServer((HOST, PORT), Handler)
print(f"[+] Listening on port {PORT}...")
server.serve_forever()