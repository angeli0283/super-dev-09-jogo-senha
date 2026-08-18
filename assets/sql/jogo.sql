CREATE DATABASE IF NOT EXISTS password_jogo;
USE password_jogo;

CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jogador_nome VARCHAR(50) NOT NULL,
    regras_completas INT NOT NULL,
    total_regras INT NOT NULL,
    senha_length INT NOT NULL,
    tempo_segundos INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_ranking ON scores (regras_completas DESC, tempo_segundos ASC);

INSERT INTO scores (jogador_nome, regras_completas, total_regras, senha_length, tempo_segundos)
VALUES ('teste', 12, 12, 20, 95);