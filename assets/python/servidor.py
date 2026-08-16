"""
servidor.py
Servidor sem Flask, usando http.server (biblioteca padrão do Python).
Agora com suporte a CORS, necessário porque o HTML é aberto como
arquivo local (file://) e o navegador bloqueia requisições pra outra
origem (localhost:8000) sem essa permissão explícita.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from regras import avaliar_todas, REGRAS
from banco import salvar_resultado, listar_placar


class MeuHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        # o navegador manda essa requisição "de teste" antes do POST de verdade,
        # perguntando se tem permissão -- sem responder isso, o POST nunca sai
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/leaderboard":
            resultados = listar_placar()
            for linha in resultados:
                linha["created_at"] = str(linha["created_at"])

            self.__responder_json(resultados)
            return

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b"Servidor no ar")

    def do_POST(self):
        tamanho_conteudo = int(self.headers.get("Content-Length", 0))
        corpo_bruto = self.rfile.read(tamanho_conteudo)
        dados = json.loads(corpo_bruto)

        if self.path == "/api/validate":
            self.__tratar_validate(dados)
        elif self.path == "/api/score":
            self.__tratar_score(dados)
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

    def __tratar_validate(self, dados):
        senha = dados.get("password", "")
        resultados = avaliar_todas(senha)
        passou_count = sum(1 for r in resultados if r["passou"])

        resposta = {
            "resultados": resultados,
            "passou_count": passou_count,
            "total_regras": len(REGRAS),
            "todas_passaram": passou_count == len(REGRAS),
        }
        self.__responder_json(resposta)

    def __tratar_score(self, dados):
        jogador_nome = dados.get("player_name", "Anônimo")
        senha = dados.get("password", "")
        tempo_segundos = int(dados.get("time_seconds", 0))

        resultados = avaliar_todas(senha)
        passou_count = sum(1 for r in resultados if r["passou"])

        salvar_resultado(
            jogador_nome=jogador_nome,
            regras_completas=passou_count,
            total_regras=len(REGRAS),
            senha_length=len(senha),
            tempo_segundos=tempo_segundos,
        )

        resposta = {"passou_count": passou_count, "total_regras": len(REGRAS)}
        self.__responder_json(resposta)

    def __responder_json(self, dados_resposta):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(dados_resposta).encode())


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8000), MeuHandler)
    print("Servidor rodando em http://localhost:8000")
    servidor.serve_forever()