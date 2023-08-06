import flet


class Text (object):
	
	def __init__(self, value="", color="white", bgcolor=None, text_align=1, size=18, font_family="default", width=100, height=40, expand_width=False, expand_height=False
	, opacity=1.0):
		self.__self_ui = flet.Text("")
		
		self.parent = None
		self.page = None
		
		self.value = value
		self.color = color
		self.bgcolor = bgcolor
		self.text_align = text_align
		self.size = size
		self.font_family = font_family
		self.x = 0
		self.width = width
		self.height = height
		self.y = 0
		self.expand_width = expand_width
		self.expand_height = expand_height
		self.opacity = opacity
		
		self.update()
	
	
	def update(self):
		l = self.__self_ui

		l.value = self.value
		l.opacity = self.opacity
		l.color = self.color
		l.bgcolor = self.bgcolor
		if self.text_align == 0:
			l.text_align = "left"
		elif self.text_align == 1:
			l.text_align = "center"
		elif self.text_align == 2:
			l.text_align = "right"
		l.size = self.size
		
		if self.font_family == "default":
			if self.page != None:
				l.font_family = self.page.font_family
		else:
			l.font_family = self.font_family
		l.width = self.width
		l.height = self.height
		
		# set the expand
		if self.parent != None:
			if self.expand_width:
				self.self_ui.width = self.parent.self_ui.width
				self.width = self.__self_ui.width
			if self.expand_height:
				self.self_ui.height = self.page.self_ui.height
		
		if self.self_ui.page == None: return
		self.self_ui.update()
		
		
	
	def respown(self, parent, page):
		self.parent = parent
		self.page = page
		self.update()
	
	
	def remove_self (self):
		self.update()
		self.parent.update()
		self.parent.remove_control (self)
	
	@property
	def self_ui(self):
		return self.__self_ui
	
	
	
	
	
	
