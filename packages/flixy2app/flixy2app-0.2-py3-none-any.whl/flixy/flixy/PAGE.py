from .Tools.action import do_action
# from .controls.SHEET import Sheet
import flet

class Page (object):
	def __init__ (self, run_as="app"):
		self.__ui_view = None
		self.__is_on_screen = True
		
		self.controls = []
		self.bgcolor = "black"
		self.title = ""
		self.__appbar = None
		self.font_family = "Avenir"
		self.width = 0
		self.height = 0
		self.spacing = 15
		
		self.touch_x = 0
		self.touch_y = 0
		
		self.on_resize = None
		self.on_touch = None
		self.on_hover = None
		self.on_update = None
		self.on_close = None
		
		self.update()
	
	def update(self):
		v = self.__ui_view
		if v == None: return
		v.bgcolor = self.bgcolor
		v.title = self.title
		
		self.width = v.width
		self.height = v.height
		
		if self.__appbar != None: self.__appbar.update()
		for control in self.controls:
			control.update()
		
		self.self_ui.update()
		do_action(self.on_update, [self])
		
	
	def add (self, flixy_control):
		if flixy_control.self_ui == None: return
		# start add
		flixy_control.respown(self, self)
		flet_control = flixy_control.self_ui
		self.controls.append(flixy_control)
		cont = flet.Row([flet_control], alignment="center")
		self.self_ui.add(cont)

		self.update()
		
	
	def clear (self):
		self.controls = []
		self.self_ui.clean()
		self.update()
	
	def show(self, target_function):
		def on_page_resize(page):
			v = self.__ui_view
			self.width = v.width
			self.height = v.height
			do_action(self.on_resize, [self])
			self.update()
		def page_app (page:flet.Page):
			self.__ui_view : flet.Page = page
			self.self_ui.on_close = self.__custom_on_close
			page.window_title_bar_hidden = True
			page.on_resize = on_page_resize
			page.horizontal_alignment = flet.MainAxisAlignment.CENTER
			self.update()
			page.update()
			target_function(self)
		flet.app(target=page_app)
	
	def close (self):
		self.self_ui.window_close()
		self.__is_on_screen = False
		do_action(self.on_close, [self])
		
	
	def reposition_controls(self):
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
	
	
	
	@property
	def appbar (self):
		return self.__appbar
	
	@appbar.setter
	def appbar(self, new_appbar):
		self.__appbar = new_appbar
		self.self_ui.appbar = new_appbar.self_ui
		new_appbar.page = self
	
	
	# propertys
	@property
	def stack(self):
		return "v"
	
	@property
	def self_ui (self) -> flet.Page:
		return self.__ui_view
	
	def on_screen (self):
		return self.__is_on_screen
	
	
	def __custom_on_close (self):
		self.__is_on_screen = False
		do_action(self.on_close, [self])
		
		
		
		
	
	
	
	
	
	
	
	
