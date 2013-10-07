# -*- coding: latin1 -*-

import webcapture, re

webcapture.acessAdress("http://www2.camara.leg.br/deputados/pesquisa")
webcapture.creatList("Deputados")

form = webcapture.getAForm("#formDepAtual")

for option in form.getValues("deputado")[:3]:

	form.setParam("deputado", option["value"])

	webcapture.acessAdress(form.action, params = form.params)
	webcapture.creatObject()

	task = webcapture.copyData("#content ul li:nth-child(1)")
	find = re.findall(r".*: (.*)", task)[0]

	webcapture.putData("nome", find)

	task = webcapture.copyData("#content ul li:nth-child(2)")
	find = re.findall(r".*: (\d*) / (\d*) - .*?:( (.*)|())", task)[0]

	webcapture.putData("aniversario", "%s/%s" % (find[0], find[1]))
	webcapture.putData("profissao", find[3])

	task = webcapture.copyData("#content ul li:nth-child(3)")
	find = re.findall(r".*: (.*?) / (.*?) / (.*)", task)[0]

	webcapture.putData("partido", find[0])
	webcapture.putData("UF", find[1])
	webcapture.putData("diplomacao", find[2])

	task = webcapture.copyData("#content ul li:nth-child(4)")
	find = re.findall(r".*: (\(\d*?\)) ([\d-]*) - Fax: ([\d-]*)", task)[0]

	webcapture.putData("telefone", find[0] + find[1])
	webcapture.putData("fax", find[0]  + find[2])

	task = webcapture.copyData("#content ul li:nth-child(5)")
	find = re.findall(r"\d{2}/\d{2}", task)

	webcapture.putData("legislaturas", find)

	img = webcapture.getTags("img", "#content .clearedBox")[0]
	webcapture.putData("foto", img.attrib["src"])

	webcapture.closeObject()

webcapture.saveData('json')