# -*- coding: latin1 -*-

import clientcontroller, sys, json

class webcapture(object):
	"""docstring for webcapture"""

	__client = clientcontroller.Client()

	__out = {}
	__stack = [__out]

	@staticmethod
	def acessAdress(adress, method = "get", **kwargs):
		webcapture.__client.acess(adress, method, kwargs)

	@staticmethod
	def saveData(fileType, fileName = ""):
		if not fileName:
			fileName = webcapture.__client.currentSite

		def saveJson():
			f = open(fileName + ".json", "w+")
			f.write(json.dumps(webcapture.__out, sort_keys=True, indent=4, separators=(',', ': ')))
			f.close()

		def saveXml():
			print webcapture.__out

		def erro():
			print "ERRO: invalid out extension"
		{"json" : saveJson, "xml" : saveXml}.get(fileType, erro)()

	#Set de Estructure

	@staticmethod
	def creatList(name = ""):
		last = webcapture.__stack[-1]

		if isinstance(last, dict):
			if name == "" :
				print "Erro: You should define a name"
				sys.exit(0)

			last.update({name : []})
			webcapture.__stack.append(last[name])
		else:
			last.append([])
			webcapture.__stack.append(last[-1])

		#return webcapture.__stack[-1]

	@staticmethod
	def creatObject(name = ""):
		last = webcapture.__stack[-1]

		if isinstance(last, dict):
			if name == "" :
				print "Erro: You should define a name"
				sys.exit(0)

			last.update({name : {}})
			webcapture.__stack.append(last[name])
		else:
			last.append({})
			webcapture.__stack.append(last[-1])

		#return webcapture.__stack[-1]

	@staticmethod
	def captureData(name, selector, cast = None):
		last = webcapture.__stack[-1]
		data = webcapture.__client.getData(selector)

		if cast != None:
			try:
				data = str(data) if cast == types.string else int(data)
			except ValueError, e:
				print "ERRO: cast problem data: %s to %s" % (data, "string" if cast == types.string else "integer")
				print e
				sys.exit(0)

		if isinstance(last, dict):
			last.update({name : data})
		else:
			last.appent(data)

	@staticmethod
	def copyData(selector):
		return webcapture.__client.getData(selector)

	@staticmethod
	def putData(name, data):
		last = webcapture.__stack[-1]

		if isinstance(last, dict):
			last.update({name : data})
		else:
			last.appent(data)

	@staticmethod
	def closeObject():
		return webcapture.__stack.pop()

	#Get html structures

	@staticmethod
	def getTags(tagName, selector):
		return webcapture.__client.getTags(tagName, selector)
		pass

	@staticmethod
	def getAForm(selector):
		return webcapture.__client.getAForm(selector)
		pass

class types(object):
	string = 0
	integer = 1
	binary = 2


acessAdress = webcapture.acessAdress

saveData = webcapture.saveData

creatList = webcapture.creatList
creatObject = webcapture.creatObject
closeObject = webcapture.closeObject

captureData = webcapture.captureData
copyData = webcapture.copyData
putData = webcapture.putData

getTags = webcapture.getTags
getAForm = webcapture.getAForm