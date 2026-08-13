// pega o elemento do html por id ( o que o usuário digita a senha)
const inputSenha = document.getElementById("senha");

// vê toda vez que alguem digita no campo de digitar senha
inputSenha.addEventListener("input", function () {
    const senhaDigitada = this.value;

    // manda a senha pro python
    fetch ("http://localhost:8000/api/validate", {
        method: "POST",
        headers: {
            "Conten-Type": "application/json"
        },
        // conteúdo que esta sendo enviado
        body: JSON.stringfy({ password: senhaDigitada })
    })
    // devolvendo resposta
    .then(function (resposta) {
        return resposta.json();
    })
    .then(function(dados) {
        console.log(dados);
    })
    // evita err se o python cair 
    .catch(function (erro) {
        console.error("Erro ao conectar com o servidor:", erro);
    });
});