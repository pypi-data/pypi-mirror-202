import flet
from ..Tools.action import do_action



class Column (object):
	
	def __init__ (self, controls=None, scroll=True, auto_end_following = False, width = 200, height = 75, bgcolor = None, expand_width = False, expand_height = False,
	border_radius = 8, spacing=5, on_scroll=None, on_update=None, opacity=1.0):
			
		
		self.parent = None
		self.page = None
		
		self.__self_ui = flet.Column()
		if controls == None:
			self.controls = []
		else:
			self.controls = controls
		self.scroll = scroll
		self.auto_end_following = auto_end_following
		self.width = width
		self.height = height
		self.bgcolor = bgcolor
		self.expand_width = expand_width
		self.expand_height = expand_height
		self.border_radius = border_radius
		self.spacing = spacing
		self.opacity = opacity
		
		self.__offset_x = 0
		self.__offset_y = 0
		self.on_scroll = on_scroll
		self.on_update = on_update
		
		self.update()
	
	def update(self):
		v = self.self_ui
		
		v.scroll = self.scroll
		v.width = self.width
		v.height = self.height
		v.opacity = self.opacity
		v.auto_scroll = self.auto_end_following

		if self.parent != None:
			if self.expand_width:
				self.self_ui.width = self.parent.self_ui.width
				self.width = self.self_ui.width
			if self.expand_height:
				self.self_ui.height = self.parent.self_ui.height
				self.height = self.self_ui.height
			v.expand = True
		
		# update sub controls
		for i in self.controls:
			i.update()
	

		if v.page != None: v.update()
		# on update
		do_action(self.on_update, [])
	
	
	
	def add (self, flixy_control):
		if flixy_control.self_ui == None: return
		# start add
		flixy_control.respown(self, self.page)
		flet_control = flixy_control.self_ui
		self.controls.append(flixy_control)
		cont = flet.Row([flet_control], alignment="center")
		self.self_ui.controls.append(cont)

		self.update()
	
	def respown (self, parent, page):
		self.parent = parent
		self.page = page
	
	def remove_self (self):
		pass
	
	def clear (self):
		self.controls = []
		self.self_ui.clean()
		self.update()
	
	def reposition_controls (self):
		pass
	
	def remake_controls (self):
		self.self_ui.clean()
		for control in self.controls:
			self.add(control)
		
		self.appbar = self.__appbar
		if self.__appbar != None: self.__appbar.update()
	
	def remove_control (self, control):
		if control not in self.controls:
			raise NameError("Cannot found this control to remove.")
		
		for i in self.self_ui.controls:
			self.self_ui.remove(i)
		self.controls.remove(control)
		
		for i in self.controls:
			self.self_ui.add(i.self_ui)
	
	# actions
	def __on_scroll (self):
		pass
	
	def __follow_the_end (self):
		pass
	
	
	@property
	def self_ui (self):
		return self.__self_ui
	
	@property
	def stack (self):
		return "v"
	
	
	@property
	def on_screen (self):
		return self.self_ui.page != None
	
	@property
	def offset (self):
		return [0, 0]
	
	
	
	
	
	
	
	
	
	
