from .PAGE import Page
import flet
import threading


class app (object):
	
	def __init__ (self, target, develop=True):
		ThePage = Page()
		ThePage.show(target)