CREATE DATABASE password_jogo;
USE password_jogo;

CREATE TABLE scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jogador_nome VARCHAR(50) NOT NULL,
    regras_completas INT NOT NULL,
    total_regras INT NOT NULL,
    senha_length INT NOT NULL,
    tempo-segundos INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);  

CREATE INDEX idx_ranking ON scores (regras_completas DESC, time_seconds ASC);


INSERT INTO scores (jogador_nome, regras_completas, total_regras, senha_length, tempo_segundos)
VALUES ('teste', 12, 12, 20, 95);

SELECT * FROM scores ORDER BY regras_completas DESC, tempo_segundos ASC LIMIT 10;