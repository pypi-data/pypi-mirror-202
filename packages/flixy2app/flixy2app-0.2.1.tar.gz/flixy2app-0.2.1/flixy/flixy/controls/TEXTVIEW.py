from ..Tools.action import do_action
import flet



class TextView (object):
	
	def __init__ (self, value="Text View", width=300, height=150, text_color="white", bgcolor="#3F3F3F", border_radius=8, font_size=18, font_family="default",
	expand_width=False, expand_height=False, opacity=1.0, selectable=True, editable=True, text_align=0):
		self.__self_ui = flet.TextField()
		
		self.parent = None
		self.page = None
		
		self.value = value
		self.width = width
		self.height = height
		self.text_color = text_color
		self.bgcolor = bgcolor
		self.border_radius = border_radius
		self.font_size = font_size
		self.font_family = font_family
		self.expand_width = expand_width
		self.expand_height = expand_height
		self.opacity = 1.0
		self.selectable = selectable
		self.editable = editable
		self.text_align = text_align
		
		self.last_char = ""
		
		self.x = 0
		self.y = 0
		
		# actions
		self.on_edit = None
		self.on_start_edit = None
		self.on_done_edit = None
		
		self.update()
	
	def update (self):
		tv = self.self_ui
		tv.multiline = True
		tv.value = self.value
		tv.width = self.width
		tv.height = self.height
		tv.color = self.text_color
		tv.bgcolor = self.bgcolor
		tv.border_radius = self.border_radius
		
		tv.opacity = self.opacity
		tv.disabled = self.editable == False
		if self.text_align == 0:
			tv.text_align = "left"
		elif self.text_align == 1:
			tv.text_align = "center"
		elif self.text_align == 2:
			tv.text_align = "right"
		
		if self.self_ui.page != None:
			tv.update()
		
	
	def respown(self, parent, page):
		self.parent = parent
		self.page = page
		self.update()
	
	def remove_self (self):
		self.update()
		self.parent.update()
		self.parent.remove_control (self)
	
	def focus (self):
		self.self_ui.focus()
	
	def stop (self):
		pass
	
	
	@property
	def self_ui(self):
		return self.__self_ui