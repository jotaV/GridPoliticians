# -*- coding: latin1 -*-

class Reader(object):
	"""docstring for Reader"""

	__clientController = ClientController()

	__out = {}
	__stack = [__out]

	def __init__(self, script, outType = None):
		self.script = script
		outType = outType if outType else "xml"

		Reader.__clientController.load(script.adress)

	def creatList(self, name = None):
		if type(Reader.__stack[-1]) != type(list):
			Reader.__stack[-1].update({name : []})
			Reader.__stack.append(Reader.__stack[-1][name])
		else:
			#Erro ao criar uma lista dentro de outra lista
			pass

	def creatObject(self, name):
		if type(Reader.__stack[-1]) != type(list):
			Reader.__stack[-1].append({})
			Reader.__stack.append(Reader.__stack[-1][-1])
		else:
			Reader.__out.update({name : {}})
			Reader.__stack.append(Reader.__stack[-1][name])

	def creatData(self, name, data):
		Reader.__out.update({name : data})
		Reader.__stack.append(Reader.__out[name])

	def captureData(self, name, selector, cast = None):
		data = Reader.__clientController.capture(selector, cast)
		Reader.creatData(name, data)

	def acessAdress(self, adress):
		Reader.__clientController.load(adress)

	def forEach(self, tagName, seletor, call):
		lastObject = len(Reader.__stack)
		currentAdress = Reader.__clientController.currentAdress

		for tag in Reader.__clientController.find(tagName, seletor):
			call(tag)
			Reader.__stack = Reader.__stack[0:lastObject]
			Reader.__clientController.currentAdress = currentAdress

	def onFunction(self, call):
		lastObject = len(Reader.__stack)
		currentAdress = Reader.__clientController.currentAdress

		call()

		Reader.__stack = Reader.__stack[0:lastObject]
		Reader.__clientController.currentAdress = currentAdress
