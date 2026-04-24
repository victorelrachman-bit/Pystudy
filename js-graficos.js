async function verificar() {
    const log = await fetch("http://127.0.0.1:5000/status", {
        credentials: "include"
    });
    const log_json = await log.json()
    if(!log_json.logado)
    {
        window.location.href = "http://127.0.0.1:5500/index.html"
    }
}

verificar()

async function tratarDados()
{
    const res = await fetch("http://127.0.0.1:5000/mostra-dados", {
        credentials: "include"
    });

    const dados = await res.json()

    const p = document.getElementById('gra')
    p.innerText = JSON.stringify(dados)
}

tratarDados()