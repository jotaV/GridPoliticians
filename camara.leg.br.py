# -*- coding: latin1 -*-

from webcapture import WebCapture

wb = WebCapture()

wb.accessUrl("http://www2.camara.leg.br/deputados/pesquisa")
wb.creatList("Deputados")

form = wb.getform("#formDepAtual")

for option in form.getValues("deputado"):

	form.setParam("deputado", option.value)
	wb.accessForm(form)

	wb.creatObject()

	wb.capture("nome", "#content ul li:nth-child(1)",
		format = "Nome civil: (.*)", filter = 1)

	wb.capture("aniversario", "#content ul li:nth-child(2)",
		format = r".*: (\d*) / (\d*) .*", filter = "\\1/\\2")

	wb.capture("profissao", "#content ul li:nth-child(2)",
		format = r".*: .*: (.*)", filter = "\\1")

	wb.capture("partido", "#content ul li:nth-child(3)",
		format = r".*: (.*?) / (.*?) / (.*)", filter = "\\1")

	wb.capture("UF", "#content ul li:nth-child(3)",
		format = r".*: (.*?) / (.*?) / (.*)", filter = "\\2")

	wb.capture("diplomacao", "#content ul li:nth-child(3)",
		format = r".*: (.*?) / (.*?) / (.*)", filter = "\\3")

	wb.capture("telefone", "#content ul li:nth-child(4)",
		format = r".*: (\(\d*?\)) ([\d-]*) .*", filter = "\\1 \\2")

	wb.capture("fax", "#content ul li:nth-child(4)",
		format = r".*: (\(\d*?\)) ([\d-]*) - Fax: ([\d-]*)", filter = "\\1 \\3")

	wb.capture("legislaturas", "#content ul li:nth-child(5)",
		find = r"\d{2}/\d{2}")

	img = wb.getTagList("#content .clearedBox", "img")[0]  #wb.capture(""#content .clearedBox img[0][src]"
	wb.put("fotolink", img.attrib["src"])

	wb.closeObject()

wb.save('json')
wb.save('xml')