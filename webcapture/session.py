# -*- coding: latin1 -*-

import requests

from urlparse import urlparse
from pyquery import PyQuery as PQ

class Session(object):
	"""
	Provide a controller in the resquest and the structure of the page.
	"""

	def __init__(self):
		self.currentSite = ""
		self.currentAdress = ""
		self.sorceCode = ""

	def request(self, url, method, **kwargs):
		"""
		Implement the request function

		:param url: URL to be request.
		:param method: method of the request.
		:param params: (optional) Dictionary or bytes to be sent in the query string for the :class:'Request'.
	    :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:'Request'.
	    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:'Request'.
	    :param cookies: (optional) Dict or CookieJar object to send with the :class:'Request'.
	    :param files: (optional) Dictionary of 'name': file-like-objects (or {'name': ('filename', fileobj)}) for multipart encoding upload.
	    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
	    :param timeout: (optional) Float describing the timeout of the request.
	    :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
	    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
	    :param verify: (optional) if "True", the SSL cert will be verified. A CA_BUNDLE path can also be provided.
	    :param stream: (optional) if "False", the response content will be immediately downloaded.
	    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
		"""
		def default(url, **kwargs):
			raise ValueError('method %s indefined' % method)

		methods = {	'get' : requests.get,
		 			'post' : requests.post,
		 			'put' : requests.put,
		 			'delete' : requests.delete,
		 			'head'	: requests.head,
		 			'options' : requests.options}

		r = methods.get(method, default)(url, **kwargs)

		if r.status_code != requests.codes.ok:
			raise Exception("site return with status code %d" % r.status_code)

		url = urlparse(r.url)

		self.encoding = r.encoding
		self.currentSite = url.hostname
		self.currentAdress = url.geturl()

		htmlsource = r.text
		self.sorceCode = PQ(htmlsource)

	def getData(self, selector):
		"""
		Return the all text in the area limitet by the selector
		"""
		tags = self.sorceCode.find(selector)
		text = PQ(tags.html()).text()
		text = text.encode(self.encoding, 'xmlcharrefreplace')
		#print text

		return text

	def getTag(self, selector, tagName = ""):
		"""
		Return the fist tag in the selector given

		:param selector: an tunerd CSS selector to indentify the location of the data
		:param tagName: (optional) the name of the tag returned
		"""

		tag = self.sorceCode.find(selector)

		if not tagName or tag.is_(tagName):
			return tag[0]

		return tag.find(tagName)

	def getTagList(self, selector, tagName = ""):
		"""
		Return a list of the tag in the selector given

		:param selector: an tunerd CSS selector to indentify the location of the data
		:param tagName: (optional) the name of the tag returned
		"""

		tag = self.sorceCode.find(selector)
		if tagName:
			tag = tag.find(tagName)

		#TODO Working on the tag list
		#...

		return tag

	def getAForm(self, selector):
		"""
		Return the fist tag in the selector given

		:param selector: an tunerd CSS selector or an number to indentify the location of the data
		"""

		form = None

		if isinstance(selector, str):
			tags = self.sorceCode.find(selector)
			if not tags[0].tag == "form":
				form = tags.find("form")[0]
			else:
				form = tags[0]

		elif isinstance(selector, int):
			try:
				form = self.sorceCode.find("form")[selector]
			except IndexError:
				raise IndexError("form index out of range in current page")

		return form


