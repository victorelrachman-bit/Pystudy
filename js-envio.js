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

const form = document.querySelector("form")

const feitas = document.querySelector('input[name="feitas"]')
const acert = document.querySelector('input[name="acert"]')

form.addEventListener("submit", (e) => {

    const feitasV = Number(feitas.value)
    const acertV = Number(acert.value)

    if (acertV > feitasV) {
        e.preventDefault()
        alert("Acertos não podem ser maiores que feitas!")
    }
})

const inputData = document.querySelector('input[name="dia"]')
const hoje = new Date().toISOString().split("T")[0]
inputData.max = hoje