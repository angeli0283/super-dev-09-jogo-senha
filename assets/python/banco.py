"""
banco.py
Segue o mesmo padrão usado no exemplo do restaurante (funcionario.py):
uma função conectar() que abre a conexão e devolve ela, chamada sempre
que alguma outra função precisa falar com o MySQL.
"""

import mysql.connector

HOST = "localhost"
PORTA = 3306
USUARIO = "root"
SENHA = "admin"
BANCO = "password_jogo"


def conectar():
    """Abre a conexão com o MySQL e retorna ela."""
    conexao = mysql.connector.connect(
        host=HOST,
        port=PORTA,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
    )
    return conexao


def salvar_resultado(jogador_nome: str, regras_completas: int, total_regras: int,
                      senha_length: int, tempo_segundos: int):
    """Grava um resultado de partida na tabela scores."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO scores
            (jogador_nome, regras_completas, total_regras, senha_length, tempo_segundos)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (jogador_nome, regras_completas, total_regras, senha_length, tempo_segundos),
    )
    conexao.commit()

    cursor.close()
    conexao.close()

def listar_placar(
    limite: int = 10,
    ordenar_por: str = "regras",
    ordem: str = "desc"
):
    """Devolve o placar com opções de ordenação."""

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    # Define o campo usado na ordenação
    campos_ordenacao = {
        "regras": "regras_completas",
        "tempo": "tempo_segundos",
        "nome": "jogador_nome",
        "data": "created_at"
    }

    campo = campos_ordenacao.get(ordenar_por, "regras_completas")

    # Define a direção da ordenação
    if ordem.lower() == "asc":
        direcao = "ASC"
    else:
        direcao = "DESC"

    sql = f"""
        SELECT 
            jogador_nome, 
            regras_completas, 
            total_regras, 
            tempo_segundos, 
            created_at 
        FROM scores 
        ORDER BY {campo} {direcao} 
        LIMIT %s 
    """

    cursor.execute(sql, (limite,))

    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados
