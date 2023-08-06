import flet
from ..Tools.action import do_action


class Button (object):
	
	def __init__ (self, title="", bgcolor="#4082ff", title_color="white", bgcolor_after_hover="#80acff", on_click=None, width=250, height=50, border_radius=15
	, font_size=16, font_family='default', opacity=1.0, expand_width=False, expand_height=False, on_hover=None):
		self.__self_ui = flet.ElevatedButton()
		
		self.page = None
		self.parent = None
		
		self.title = title
		self.bgcolor = bgcolor
		self.title_color = title_color
		self.bgcolor_after_hover = bgcolor_after_hover
		self.width = width
		self.height = height
		self.border_radius = border_radius
		self.font_size = font_size
		self.font_family = font_family
		self.opacity = opacity
		self.expand_width = expand_width
		self.expand_height = expand_height
		
		# actions
		self.on_click = on_click
		self.on_hover = on_hover
		
		self.update()
	
	def update(self):
		v = self.self_ui
		
		v.bgcolor = self.bgcolor
		# v.border_radius = self.border_radius
		v.width = self.width
		v.height = self.height
		v.opacity = self.opacity
		v.on_click = self.__on_click
		v.on_hover = self.__on_hover
		
		v.text = self.title
		v.color = self.title_color
		
		# set the expand
		if self.parent != None:
			if self.expand_width:
				self.__self_ui.width = self.parent.self_ui.width
				self.width = self.__self_ui.width
			if self.expand_height:
				self.self_ui.height = self.parent.self_ui.height
			if self.expand_height and self.expand_width:
				v.expand = True


		if self.self_ui.page == None: return
		v.update()
	
	def respown (self, parent, page):
		self.parent = parent
		self.page = page
	
	def remove_self (self):
		self.update()
		self.parent.update()
		self.parent.remove_control (self)
	
	
	def __on_hover(self, event):
		do_action(self.on_hover, [self])
	
	
	def __on_click(self, event):
		do_action(self.on_click, [self])
	
	@property
	def self_ui(self):
		return self.__self_ui














