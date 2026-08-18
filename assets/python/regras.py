"""
regras.py 
Cada regra é uma função separada (mesmo padrão de funções pequenas 
e objetivas do repositório de referência). Depois, juntamos todas 
numa lista de dicionários -- igual ao padrão usado em 
exemplo_05_dicionario.py (Dict com chaves nomeadas) e na Loja do 
exemplo_06_classes.py (lista de dicionários guardando cada item). 
"""

from typing import Callable, Dict, List 
import re 
 
 
def regra_tamanho_minimo(senha: str) -> bool: 
    return len(senha) >= 5 
 
def regra_tamanho_maximo(senha: str) -> bool: 
    return len(senha) <= 10 
 
def regra_numero_romano(senha: str) -> bool: 
    return bool(re.search(r"[XVICLDM]", senha))  
 
def regra_tem_numero(senha: str) -> bool: 
    return any(caractere.isdigit() for caractere in senha) 
 
 
def regra_tem_maiuscula(senha: str) -> bool: 
    return any(caractere.isupper() for caractere in senha) 
 
 
def regra_tem_especial(senha: str) -> bool: 
    return bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};:'\",.<>/?]", senha)) 
 
 
def regra_digitos_somam_25(senha: str) -> bool: 
    digitos = [int(c) for c in senha if c.isdigit()] 
    return sum(digitos) == 25 
 
 
# Lista de regras: cada item é um dicionário com "mensagem" e "teste", 
REGRAS: List[Dict[str, object]] = [ 
    {"mensagem": "A senha deve ter pelo menos 5 caracteres.", "teste": regra_tamanho_minimo}, 
    {"mensagem": "A senha deve conter um número.", "teste": regra_tem_numero}, 
    {"mensagem": "A senha deve conter uma letra maiúscula.", "teste": regra_tem_maiuscula}, 
    {"mensagem": "A senha deve conter um caractere especial.", "teste": regra_tem_especial}, 
    {"mensagem": "Os dígitos da senha devem somar exatamente 25.", "teste": regra_digitos_somam_25}, 
    {"mensagem": "A senha deve ter no maximo 10 caracteres.", "teste": regra_tamanho_maximo }, 
    {"mensagem": "A senha deve ter pelo menos 1 numero Romano", "teste": regra_numero_romano}  
] 
 
 
def avaliar_todas(senha: str) -> List[Dict[str, object]]: 
    """Roda todas as regras e devolve o resultado de cada uma.""" 
    resultados = [] 
    for regra in REGRAS: 
        funcao_teste: Callable[[str], bool] = regra["teste"] 
        passou = funcao_teste(senha) 
        resultados.append({"mensagem": regra["mensagem"], "passou": passou}) 
    return resultados