# -*- coding: latin1 -*-

"""
A simple script to get a list of links in a site, in this case 'http://www.cms.ba.gov.br/vereadores.aspx', execute each and get some data in its respective pages

Um script simples para obter uma lista de links em um site, neste caso 'http://www.cms.ba.gov.br/vereadores.aspx', execute cada um e obter alguns dados em suas respectivas páginas
"""

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