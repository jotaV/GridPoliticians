import webcapture

webcapture.acessAdress("http://www.cms.ba.gov.br/vereadores.aspx")
webcapture.creatList("Vereadores")

for tag in webcapture.getTags("a", "#meio_conteudo .foto_vereador_int"):

	webcapture.acessAdress(tag.attrib["href"])

	webcapture.creatObject()
	webcapture.captureData("nome", ".nome_vereador")
	webcapture.captureData("cargo", ".cargo_ver")
	webcapture.captureData("partido", ".partido_vereador")
	webcapture.captureData("telefone", ".telefones_vereador")
	webcapture.captureData("email", ".email_vereador")
	webcapture.captureData("image", ".quebra_esq > img[src]", webcapture.types.bin)
	webcapture.closeObject()

webcapture.saveData('json')