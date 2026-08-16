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
SENHA = "sua_senha_mysql"
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


def listar_placar(limite: int = 10):
    """Devolve os melhores resultados, igual listar_funconarios() faz pra funcionários."""
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)  # dictionary=True -> cada linha vira um dict

    cursor.execute(
        """
        SELECT jogador_nome, regras_completas, total_regras, tempo_segundos, created_at
        FROM scores
        ORDER BY regras_completas DESC, tempo_segundos ASC
        LIMIT %s
        """,
        (limite,),
    )
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados