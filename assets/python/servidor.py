from http.server import BaseHTTPRequestHandler, HTTPServer
import json 
import mysql.connector 

#conexão com html e js 

class MeuHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Servidor no ar")


    def do_POST(self):
        tamanho_conteudo = int(self.header.get("Content-length", 0))
        corpo_bruto = self.rfile.read(tamanho_conteudo)
        dados = json.loads(corpo_bruto)
        senha = dados.get("senha", "")
        print("Senha recebida", senha)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        resposta = {"Senha recebida": senha}
        self.wfile.write(json.dumps(resposta) .encode())


servidor = HTTPServer(("localhost", 8000), MeuHandler)
servidor.serve_forever()

# conexão com banco de dados 

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    senha="sua_senha_mysql",
    database="password_jogo"
)

cursor = conexao.cursor()
cursor 