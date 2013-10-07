# -*- coding: latin1 -*-

"""
webcapture library
==================

Simple way to capture data in any site with.
"""

__title__ = 'nada'
__author__ = 'j0tave - João Vitor'

try:
	import requests
except ImportError:
	raise ImportError("Must need install the library requests")

try:
	import requests
except ImportError:
	raise ImportError("Must need install the library requests")

from .webcapture import WebCapture
from .structures import Form
