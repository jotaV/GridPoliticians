from xml.etree import ElementTree

class Dict2XML(ElementTree.ElementTree):
	"""
	Dict2XML
	========

	Convert a Dict structure in XML using ElementTree.ElementTree structure

	>>> xml = Dict2XML({'name': 'john', 'phone': '555-7982'})
	>>> xml.write(sys.stdout)
	<root><phone>555-7982</phone><name>john</name></root>
	>>> xml.find('name').text
	'john'

	>>> xml = Dict2XML({'agelist': [{'name': 'Van Damme', 'age': 52},
	... {'name': 'Stallone', 'age': 67},
	... {'name': 'Clint Eastwood', 'age': 83}]})
	>>> map(lambda x: x.text, list(xml.iter('age')))
	['52', '67', '83']
	"""

	def __init__(self, xmldict):
		rootdict = {'root' : xmldict}
		roottag = rootdict.keys()[0]
		root = ElementTree.Element(roottag)

		self._ConvertDictToXmlRecurse(root, rootdict[roottag])

		ElementTree.ElementTree.__init__(self, root)

	def _ConvertDictToXmlRecurse(self, parent, dictitem):
		assert type(dictitem) is not type([])

		if isinstance(dictitem, dict):
		    for (tag, child) in dictitem.iteritems():

		        if str(tag) == '_text':
		       	    parent.text = unicode(child)

		        elif type(child) is type([]):
		            # iterate through the array and convert

		            for listchild in child:
		                elem = ElementTree.Element(tag)
		                parent.append(elem)
		                self._ConvertDictToXmlRecurse(elem, listchild)

		        else:
		            elem = ElementTree.Element(tag)
		            parent.append(elem)
		            self._ConvertDictToXmlRecurse(elem, child)

		else:
		    parent.text = unicode(dictitem)
