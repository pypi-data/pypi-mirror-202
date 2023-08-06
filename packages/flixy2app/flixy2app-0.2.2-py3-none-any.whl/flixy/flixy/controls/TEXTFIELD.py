from ..Tools.action import do_action
from ..Tools.convert_rgb_to_hex import hex_to_rgb
import flet


class TextField (object):
	
	def __init__ (self, value="", placeholder="Type..", width=300, height=50, text_color="black", bgcolor=None, border_radius=15, font_size=18, font_family="default",
	expand_width=False, expand_height=False, opacity=1.0, selectable=True, editable=True, text_align=0, autocorrection=False):
		
		self.__self_ui = flet.TextField(on_change=self.__custom_on_edit, on_focus=self.__custom_on_start, 
		on_submit=self.__custom_on_done_edit)
		
		self.parent = None
		self.page = None
		
	
		self.value = value
		self.placeholder = placeholder
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
		self.autocorrection = autocorrection
		
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
		tv.autocorrection_type = self.autocorrection
		tv.value = self.value
		tv.label = self.placeholder
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
		self.self_ui.end_editing()
	
	def __custom_on_edit(self, *args):
		self.value = self.self_ui.value
		do_action(self.on_edit, [self])
	
	def __custom_on_start (self, *args):
		do_action(self.on_start_edit, [self])
	
	def __custom_on_done_edit (self, *args):
		self.value = self.self_ui.value
		do_action(self.on_done_edit, [self])
	
	
	@property
	def self_ui(self):
		return self.__self_ui






# delegate
class textViewDelegate (object):
	def __init__ (self, self_class):
		self.self_class = self_class
	def textfield_should_begin_editing(self, textfield):
		return True
	def textfield_did_begin_editing(self, textfield):
		do_action(self.self_class.on_start_edit, [self.self_class])
	def textfield_did_end_editing(self, textfield):
		return True
	def textfield_should_return(self, textfield):
		textfield.end_editing()
		do_action(self.self_class.on_done_edit, [self.self_class])
		return True
	def textfield_should_change(self, textfield, range, replacement):
		self.self_class.last_char = replacement
		return True
	def textfield_did_change(self, textfield):
		self.self_class.value = textfield.text
		do_action(self.self_class.on_edit, [self.self_class])
		return True


















