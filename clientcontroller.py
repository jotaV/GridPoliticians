# -*- coding: latin1 -*-

import requests, sys
from pyquery import PyQuery
#from HTMLParser import HTMLParser

class Client(object):
	"""docstring for ClientController"""

	def __init__(self):
		self.currentSite = ""
		self.currentAdress = ""
		self.sorceCode = ""

	def acess(self, url, method, kwargs):
		def default(url, **kwargs):
			print "ERRO: method %s indefined" % method
			sys.exit(0)

		methods = {	'get' : requests.get,
		 			'post' : requests.post,
		 			'put' : requests.put,
		 			'delete' : requests.delete,
		 			'head'	: requests.head,
		 			'options' : requests.options}

		request = methods.get(method, default)(url, **kwargs)

		if request.status_code != requests.codes.ok:
			print "ERRO: site with status code %d" % request.status_code
			sys.exit(0)

		url = request.url
		self.currentSite = url[url.index('/') + 2:url.index('/', 7)]
		self.currentAdress = request.url

		self.sorceCode = PyQuery(request.text)

	def getData(self, selector):
		tags = self.sorceCode.find(selector)
		text = PyQuery(tags.html()).text()
		text = text.encode('utf-8', 'xmlcharrefreplace')

		return text

	def getTags(self, tagName, selector):
		tags = self.sorceCode.find(selector).find(tagName)
		return tags

	def getAForm(self, selector):
		tags = self.sorceCode.find(selector)
		form = None

		if isinstance(selector, str):
			if not tags.is_("form"):
				form = tags.find("form")[0]
			else:
				form = tags[0]

		elif isinstance(selector, int):
			try:
				form = PyQuery(self.sorceCode.find("form")[selector])
			except IndexError:
				print "ERRO: form index out of range"

		return Form(form)

class Form(object):

	def __init__(self, sorce):
		self.sorce = sorce

		if "action" in sorce.attrib:
			self.action = sorce.attrib["action"]
		else:
			print "ERRO: the <form> don't have action attribute"

		if "method" in sorce.attrib:
			self.method = sorce.attrib["method"]
		else:
			self.method = "get"

		self.params = {}
		self.options = {}

		self.checkParams(PyQuery(self.sorce))

	def checkParams(self, source):

		for child in source.children():
			valid = ["input",
					"textarea",
					"select"]

			if child.tag in valid and "name" in child.attrib:

				name = child.attrib["name"]
				block = True if "checked" in child.attrib and child.attrib["checked"] == "checked" else False

				if not name in self.params or block:
					value = child.attrib["value"] if "value" in child.attrib else ""

					self.params.update({name : value})

				if child.tag == "select":
					valueList = []
					options = PyQuery(child).find("option")

					def map(i, e):
						if "value" in e.attrib and e.attrib["value"] != "":
							valueList.append({"value" : e.attrib["value"],
											 "text" : e.text})

					options.map(map)
					self.options.update({name : valueList})
			else:
				self.checkParams(PyQuery(child))

	def getValues(self, param):
		if param in self.options:
			return self.options[param]
		else:
			print "ERRO: variable %s not found in the <form>" % param

	def getParam(self, param):
		if param in self.params:
			return self.params[param]
		else:
			print "ERRO: variable %s not found in the <form>" % param

	def setParam(self, param, value):
		if param in self.params:
			self.params[param] = value
		else:
			print "ERRO: variable %s not found in the <form>" % param


