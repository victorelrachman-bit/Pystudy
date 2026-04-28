async function verificar() {
    const log = await fetch("http://127.0.0.1:5000/status", {
        credentials: "include"
    });

    const log_json = await log.json()

    if(!log_json.logado) {
        window.location.href = "http://127.0.0.1:5500/index.html"
    }
}

function criarGraf(dias, tempo, car) {
    const ctx = document.getElementById('grap-'+car[0]).getContext('2d')

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dias,
            datasets: [{
                label: "Tempo de estudo " + car,
                data: tempo,
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,  
            maintainAspectRatio: false,
            scales: {
                y:{
                    ticks:{
                        callback: function (value){
                            return value + " min"
                        }
                    }
                }
            }
        }
    })
}

async function tratarDados() {
    const res = await fetch("http://127.0.0.1:5000/mostra-dados", {
        credentials: "include"
    });
    const dados = await res.json()

    //mat
    const mat = dados.mat || []
    const dias_m = mat.map(item => {
        const d = new Date(item.dia)
        return d.toLocaleDateString('pt-br')
    })
    const tempo_m = mat.map(item => item.tempo)
    criarGraf(dias_m, tempo_m, 'matemática')

    //ing
    const ing = dados.ing || []
    const dias_i = ing.map(item => {
        const d = new Date(item.dia)
        return d.toLocaleDateString('pt-br')
    })
    const tempo_i = ing.map(item => item.tempo)
    criarGraf(dias_i, tempo_i, 'inglês')

    //prog
    const prog = dados.prog || []
    const dias_p = prog.map(item => {
        const d = new Date(item.dia)
        return d.toLocaleDateString('pt-br')
    })
    const tempo_p = prog.map(item => item.tempo)
    criarGraf(dias_p, tempo_p, 'programação')
}

async function iniciar() {
    await verificar()
    await tratarDados()
}

iniciar()