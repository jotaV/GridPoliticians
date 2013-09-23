adress = "http://www2.camara.leg.br/deputados/pesquisa"

def onInit():
	creatList("Vereadores")
	forEach("a", "#meio_conteudo.foto_vereador_int", goVereadores)

def goVereadores(tag):
	acessAdress(tag.href)

	creatObject()
	captureData("name", ".nome_vereador")
	captureData("cargo", ".nome_vereador")
	captureData("partido", ".nome_vereador")
	captureData("telefone", ".telefones_vereador")
	captureData("email", ".email_vereador")
	captureData("image", ".quebra_esq>img[src]")