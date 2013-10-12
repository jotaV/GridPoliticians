# -*- coding: latin1 -*-

"""
Script with the main structures of the module
"""

from urlparse import urljoin
from xml.etree import ElementTree

class Form(ElementTree.Element):
	"""
	Class of an instace of the form tag. Give a simple control of the form

	>>> from pyquery import PyQuery as PQ
	>>> f = PQ('<html><form action="demo_form.asp">' +
	... 'First name: <input type="text" name="FirstName" value="Mickey"><br>' +
	... 'Last name: <input type="text" name="LastName" value="Mouse"><br>' +
	... '<input type="submit" value="Submit"></form></html>')
	>>> form = Form(f.find('form')[0])
	>>> form.params
	{'LastName': 'Mouse', 'FirstName': 'Mickey'}
	>>> form.options
	{}
	>>> form.setParam('FirstName', 'Minnie')
	>>> form.getParam('FirstName')
	'Minnie'
	"""
	validChildren = ("input", "textarea", "select")

	class Option():
		"""
		Simple class for define a list of options in the Form
		"""

		def __init__(self, name, value):
			self.name = name
			self.value = value

	def __init__(self, form, url):
		"""
		:param form: an :class:ElementTree.Element of a tag form
		"""

		ElementTree.Element.__init__(self, 'form')
		self.attrib = form.attrib
		self.extend(form)

		if "action" in self.attrib:
			self.action = urljoin(url, self.attrib["action"])
		else:
			print "Warning: the <form> don't have action attribute"

		if "method" in self.attrib:
			self.method = self.attrib["method"]
		else:
			self.method = "get"

		self.params = {}
		self.options = {}

		self.checkParams(self)

	def checkParams(self, current):
		"""
		An function of process the form structure recursively
		"""

		for child in current.getchildren():

			if child.tag in Form.validChildren and "name" in child.attrib:
				name = child.attrib["name"]
				block = True if "checked" in child.attrib and child.attrib["checked"] == "checked" else False
				value = child.attrib["value"] if "value" in child.attrib else ""

				if name in self.params:
					if not name in self.options:
						self.options.update({name : [self.params[name], value]})
					else:
						self.options[name].append(value)

				if not name in self.params or block:
					value = child.attrib["value"] if "value" in child.attrib else ""
					self.params.update({name : value})

				if child.tag == 'select':
					self.select(child, name)

			else:
				self.checkParams(child)

	def select(self, child, name):
		"""
		select tag treatment for identify possible options

		:param child: the tag
		:param name: the attribute name of the tag
		"""
		valueList = []
		options = child.findall("option")

		def mapOptions(e):
			if "value" in e.attrib and e.attrib["value"]:
				valueList.append(self.Option(e.text, e.attrib["value"]))

		map(mapOptions, options)
		self.options.update({name : valueList})

	def getValues(self, param):
		"""
		Return an list with all possibles options for the parameter givem

		:param param: the name of the parameter
		"""

		if param in self.options:
			return self.options[param]
		else:
			raise ValueError("Seems that parameter %s don't have options" % param)

	def getParam(self, param):
		"""
		Return the current value of the parameter

		:param param: the name of the parameter
		"""

		if param in self.params:
			return self.params[param]
		else:
			raise ValueError("Parameter %s not found in the <form>" % param)

	def setParam(self, param, value):
		"""
		Return the current value of the parameter

		:param param: the name of the parameter
		:param value: a value for the parameter
		"""

		if param in self.params:
			self.params[param] = value
		else:
			raise ValueError("Parameter %s not found in the <form>" % param)
