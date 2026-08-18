const inputSenha = document.getElementById("senha");
const listaRegras = document.getElementById("listaRegras");
const painelVitoria = document.getElementById("painelVitoria");
const botaoSalvar = document.getElementById("botaoSalvar");
const nomeJogadorInput = document.getElementById("nomeJogador");
const tabelaPlacarBody = document.querySelector("#tabelaPlacar tbody");

const inicio = Date.now();

// controla quantas regras já foram "desbloqueadas" e estão visíveis na tela.
// começa em 1: a pessoa sempre vê ao menos a primeira regra.
let regrasReveladas = 1;

inputSenha.addEventListener("input", function () {
    const senhaDigitada = this.value;

    fetch("http://localhost:8000/api/validate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password: senhaDigitada })
    })
        .then(function (resposta) {
            return resposta.json();
        })
        .then(function (dados) {
            atualizarRevelacao(dados.resultados);
            mostrarRegras(dados.resultados);

            if (dados.todas_passaram) {
                painelVitoria.style.display = "block";
            } else {
                painelVitoria.style.display = "none";
            }
        })
        .catch(function (erro) {
            console.error("Erro ao conectar com o servidor:", erro);
        });
});

// decide se libera a próxima regra: só libera quando TODAS as regras
// já reveladas até agora estão passando (dados.resultados vem na mesma
// ordem da lista REGRAS do backend, então dá pra usar o índice)
function atualizarRevelacao(resultados) {
    const totalRegras = resultados.length;

    // pega só as regras que já estão visíveis no momento
    const regrasAtuaisVisiveis = resultados.slice(0, regrasReveladas);

    const todasVisiveisPassaram = regrasAtuaisVisiveis.every(function (regra) {
        return regra.passou;
    });

    if (todasVisiveisPassaram && regrasReveladas < totalRegras) {
        regrasReveladas = regrasReveladas + 1;
    }
}

// desenha só as regras já reveladas, não a lista inteira
function mostrarRegras(resultados) {
    listaRegras.innerHTML = "";

    const regrasParaMostrar = resultados.slice(0, regrasReveladas);

    regrasParaMostrar.forEach(function (regra) {
        const item = document.createElement("li");
        item.textContent = (regra.passou ? "✅ " : "❌ ") + regra.mensagem;
        listaRegras.appendChild(item);
    });
}

botaoSalvar.addEventListener("click", function () {
    const tempoSegundos = Math.floor((Date.now() - inicio) / 1000);

    fetch("http://localhost:8000/api/score", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            player_name: nomeJogadorInput.value || "Anônimo",
            password: inputSenha.value,
            time_seconds: tempoSegundos
        })
    })
        .then(function (resposta) {
            return resposta.json();
        })
        .then(function (dados) {
            // se o servidor mandou um erro, ele vem como { erro: "..." },
            // não como o resultado esperado -- checa isso antes de seguir
            if (dados.erro) {
                console.error("Servidor retornou erro ao salvar:", dados.erro);
                return;
            }
            carregarPlacar();
        })
        .catch(function (erro) {
            console.error("Erro ao salvar placar:", erro);
        });
});

function carregarPlacar() {
    fetch("http://localhost:8000/api/leaderboard")
        .then(function (resposta) {
            return resposta.json();
        })
        .then(function (linhas) {
            // mesma checagem: se veio { erro: "..." } em vez de uma lista,
            // mostra a mensagem em vez de tentar rodar .forEach nela
            if (linhas.erro) {
                console.error("Servidor retornou erro ao carregar placar:", linhas.erro);
                tabelaPlacarBody.innerHTML =
                    "<tr><td colspan='3'>Erro ao carregar placar: " + linhas.erro + "</td></tr>";
                return;
            }

            tabelaPlacarBody.innerHTML = "";

            linhas.forEach(function (linha) {
                const tr = document.createElement("tr");
                tr.innerHTML =
                    "<td>" + linha.jogador_nome + "</td>" +
                    "<td>" + linha.regras_completas + "/" + linha.total_regras + "</td>" +
                    "<td>" + linha.tempo_segundos + "</td>";
                tabelaPlacarBody.appendChild(tr);
            });
        })
        .catch(function (erro) {
            console.error("Erro ao carregar placar:", erro);
        });
}

carregarPlacar();