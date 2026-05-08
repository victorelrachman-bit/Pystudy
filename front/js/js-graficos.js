async function verificar() {
    try{
        const log = await fetch("http://127.0.0.1:5000/status", {
            credentials: "include"
        });

        const log_json = await log.json()

        if(!log_json.logado) {
            window.location.href = "http://127.0.0.1:5500/index.html"
        }
    }catch(error)
    {
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
            responsive: true,  
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

function criarGraf2C(dias, feitas, acertos, car) {
    const ctx = document.getElementById('grap2C-' + car[0]).getContext('2d')

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dias,
            datasets: [
                {
                    label: "Questões feitas",
                    data: feitas,
                    borderWidth: 1
                },
                {
                    label: "Questões acertadas",
                    data: acertos,
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return value + " qts"
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

    // MATEMÁTICA
    const mat = dados.mat || []
    const dias_m = mat.map(item => new Date(item.dia).toLocaleDateString('pt-br'))
    const tempo_m = mat.map(item => item.tempo)
    const acert_m = mat.map(item => item.acertos)
    const feitas_m = mat.map(item => item.feitas)

    criarGraf(dias_m, tempo_m, 'matemática')
    criarGraf2C(dias_m, feitas_m, acert_m, 'matemática')

    // INGLÊS
    const ing = dados.ing || []
    const dias_i = ing.map(item => new Date(item.dia).toLocaleDateString('pt-br'))
    const tempo_i = ing.map(item => item.tempo)
    const acert_i = ing.map(item => item.acertos)
    const feitas_i = ing.map(item => item.feitas)

    criarGraf(dias_i, tempo_i, 'inglês')
    criarGraf2C(dias_i, feitas_i, acert_i, 'inglês')

    // PROGRAMAÇÃO
    const prog = dados.prog || []
    const dias_p = prog.map(item => new Date(item.dia).toLocaleDateString('pt-br'))
    const tempo_p = prog.map(item => item.tempo)
    const acert_p = prog.map(item => item.acertos)
    const feitas_p = prog.map(item => item.feitas)

    criarGraf(dias_p, tempo_p, 'programação')
    criarGraf2C(dias_p, feitas_p, acert_p, 'programação')
}

async function iniciar() {
    await verificar()
    await tratarDados()
}

iniciar()