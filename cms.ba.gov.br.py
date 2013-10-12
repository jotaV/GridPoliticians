from webcapture import WebCapture

wb = WebCapture()

wb.accessUrl("http://www.cms.ba.gov.br/vereadores.aspx")
wb.creatList("Vereadores")

for tag in wb.getTagList("#meio_conteudo .foto_vereador_int", "a"):

	wb.accessUrl("http://www.cms.ba.gov.br/" + tag.attrib["href"])

	wb.creatObject()
	wb.capture("nome", ".nome_vereador")
	wb.capture("cargo", ".cargo_ver")
	wb.capture("partido", ".partido_vereador")
	wb.capture("telefone", ".telefones_vereador")
	wb.capture("email", ".email_vereador")
	wb.closeObject()

wb.save('json')
wb.save('xml')