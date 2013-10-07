# -*- coding: latin1 -*-

import json

from . import dict2xml
from .session import Session
from .structures import Form

class WebCapture(object):
	"""
	A controller of the structure of out and the request of the data
	"""

	# Main methods

	def __init__(self):
		self.__session = Session()
		self.__data = {}
		self.__stack = [self.__data]

	def accessUrl(self, url, method = "get", **kwargs):
		"""
		Set the accessed site

		:param url: URL to be request.
		:param method: method of the request.

	    See more param in :method:'Session.request'

		"""

		self.__session.request(url, method, **kwargs)

	def accessForm(self, form):
		"""
		Set the acessed site using an form

		:param form: :class:'Form' object.
		"""

		if not isinstance(form, Form):
			raise TypeError("You need pass a Form object")

		self.__session.request(form.action, form.method, params = form.params)

	def save(self, fileType, fileName = ""):
		"""
		Save de out data in a file

		:param fileType: a string to define the extesion of the file, can be 'xml' or 'json'
		:param fileName: (optional) define the name of the file. Default use the last adress acessed
		"""

		if not fileName:
			fileName = self.__session.currentSite

		if fileType == "json":
			outfile = open(fileName + ".json", "w")
  			json.dump(self.__data, outfile, encoding="utf_8", indent=4, separators=(',', ': '))
  			outfile.close()

  		elif fileType == "xml":
  			xml = dict2xml.Dict2XML(self.__data)
  			xml.write(fileName + ".xml", "UTF-8", True)

  		else:
  			print "ERRO: invalid outfile extension"
  			pass

  		# Getters an Setters

	@property
	def data(self):
		return self.__data

  	# Estructure methods

  	def creatList(self, name = "", **kwargs):
		"""
		Creat a list in the last object in the stack of out data
		:param name: the name of the new list, if the last structure in the stack or the object \
		passed is a list don't need specify a name
		:param putin: (optional) an anouther structure to cleat a list inside it.
		"""

  		last = kwargs['putin'] if 'putin' in kwargs else self.__stack[-1]

		if isinstance(last, dict):
			if name == "" :
				raise NameError('A name of the list must be defined')

			last.update({name : []})
			self.__stack.append(last[name])

		elif isinstance(last, list):
			last.append([])
			self.__stack.append(last[-1])

		else:
			raise TypeError("The parent of the list must be a list or a dict")

	def creatObject(self, name = "", **kwargs):
		"""
		Creat a object in the last object in the stack of out data
		:param name: the name of the new object, if the last structure in the stack or the object \
		passed is a list don't need specify a name
		:param putin: (optional) an anouther structure to cleat a object inside it.
		"""

		last = kwargs['putin'] if 'putin' in kwargs else self.__stack[-1]

		if isinstance(last, dict):
			if name == "" :
				raise NameError('A name of the object must be defined')

			last.update({name : {}})
			self.__stack.append(last[name])

		elif isinstance(last, list):
			last.append({})
			self.__stack.append(last[-1])

		else:
			raise TypeError("The parent of the object must be a list or a dict")

	def closeObject(self):
		"""
		Remove the last object in the stack
		"""

		return self.__stack.pop()

	# capture methods

	def capture(self, name, selector, cast = None):
		"""
		Capture and immediately save a data of the current site.
		:param name: name for the data that will be saved
		:param selector: an tunerd CSS selector to indentify the location of the data
		:param cast: (optional) a type to cast the data

		>>> wb = WebCapture()
		>>> wb.accessUrl('http://www.worldtimeserver.com/current_time_in_UTC.aspx')
		>>> wb.capture('utc time', '.font7')
		>>> print wb.data
		... # doctest: +ELLIPSIS
		{'utc time': ...}
		"""

		self.put(name, self.copy(name, selector, cast))

	def copy(self, name, selector, cast = None):
		"""
		Capture and return a data of the current site.
		:param name: name for the data that will be saved
		:param selector: an tunerd CSS selector to indentify the location of the data
		:param cast: (optional) a type to cast the data

		>>> wb = WebCapture()
		>>> wb.accessUrl('http://example.com/')
		>>> wb.copy('utc time', 'h1')
		'Example Domain'
		"""

		data = self.__session.getData(selector)

		if cast != None:
			try:
				data = cast(data)
			except ValueError, e:
				print "Cast problem data: %s to %s" % (data, cast)
				print e

		return data

	def put(self, name, data):
		"""
		Put some data in the structure
		:param name: name for the data that will be saved
		:param data: can be a string, interger, dict and list (Not will be added in the stack)

		>>> wb = WebCapture()
		>>> wb.put('my name', 'jotave')
		>>> wb.data
		'{'my name': 'jotave'}'
		>>> import datetime
		>>> wb.put('data', datetime.date.today())
		Traceback (most recent call last):
			...
		TypeError: The data parameter must be of a valid type
		"""

		if not type(data) in [str, unicode, int, dict, list]:
			raise TypeError("The data parameter must be of a valid type")

		last = self.__stack[-1]

		if isinstance(last, dict):
			last.update({name : data})
		else:
			last.appent(data)

	#Work with HTML

	def getTagList(self, tag, selector):
		"""
		Return a list of :class:'SimpleTags' in the selector given
		:param tag: a tag name
		:param selector: an tunerd CSS selector to indentify the location of the data
		"""
		pureTag = self.__session.getTagList(tag, selector)
		return pureTag

	def getform(self, selector):
		"""
		Return a  :class:'Form' in the selector given
		:param selector: an tunerd CSS selector to indentify the location of the data

		>>> wb = WebCapture()
		>>> wb.accessUrl('https://github.com/login')
		>>> form = wb.getform('#login')
		>>> form.method
		'post'
		>>> form.params
		'{'login': None, 'password': None}'
		"""
		pureForm = self.__session.getAForm(selector)
		return Form(pureForm)

