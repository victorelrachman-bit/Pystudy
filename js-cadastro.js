const parametros = new URLSearchParams(window.location.search)
const erro = parametros.get("erro")

if(erro == "usuario_existe")
{
    alert("Usuário já cadastrado!")
}
