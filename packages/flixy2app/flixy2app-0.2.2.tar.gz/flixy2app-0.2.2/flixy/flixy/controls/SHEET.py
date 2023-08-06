from .COLUMN import Column
from ..Tools.action import do_action
import flet
import time


class Sheet (object):
	
	def __init__ (self, show=False, on_hide=None):
		self.__self_ui = flet.AlertDialog(on_dismiss=self.__custom_hide)
		self.__cont = flet.Column(expand=True, width=400, height=400)
		self.self_ui.content = self.__cont
		
		self.page : flet.Page = None
		self.spacing = 10
		self.controls = []
		
		# actions
		self.on_hide = on_hide
		
		self.update()
		
		if show:
			self.show()
	
	def update (self):
		v = self.self_ui

		if self.self_ui.page != None:
			v.update()
	
	def add (self, *flixy_control):
		# start add
		for i in flixy_control:
			if i.self_ui == None: return
			i.respown(self, self.page)
			flet_control = i.self_ui
			self.controls.append(i)
			cont = flet.Row([flet_control], alignment="center")
			self.__cont.controls.append(cont)

			self.update()
		
	
	def show (self, *args):
		if self.page != None:
			self.page.self_ui.dialog = self.self_ui
			self.self_ui.open = True
			self.page.self_ui.update()

	
	def hide (self, *args):
		if self.page != None:
			self.page.self_ui.dialog = self.self_ui
			self.self_ui.open = False
			self.page.self_ui.update()
			self.__custom_hide()

	
	def __custom_hide (self, *args):
		do_action(self.hide, [])
	
	def respown(self, parent, page):
		self.page = page
		self.update()
	
	
	def remove_self (self):
		self.update()
		self.page.update()
		self.page.remove_control (self)
	
	def reposition_controls (self):
		pass
	
	def remake_controls (self):
		pass
	
	def remove_control (self, control):
		self.self_ui.clean()
		for control in self.controls:
			self.add(control)
		
		self.appbar = self.__appbar
		if self.__appbar != None: self.__appbar.update()
	
	@property
	def self_ui(self):
		return self.__self_ui
	
	@property
	def height (self):
		return self.self_ui.height
	
	@property
	def width (self):
		return self.self_ui.width
	
	@property
	def stack (self):
		return "v"
	

