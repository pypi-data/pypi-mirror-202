from ..Tools.action import do_action
import flet

class AppBar ():
	
	def __init__ (self, title="", title_size=23, title_color="white", bgcolor=None, center_title=False, on_click_btn=None, btn_icon='typb:Feed', icon_color="white"):
		self.page = None
		self.__self_ui = flet.AppBar()
		self.__title_label = flet.Text("")
		self.__bar_btn = flet.IconButton(icon=flet.icons.QUESTION_MARK_ROUNDED, on_click=self.__custom_bar_action)
		
		self.self_ui.title = self.__title_label
		self.self_ui.actions = [self.__bar_btn, flet.Text("				")]
		
		self.title = title
		self.title_size = title_size
		self.bgcolor = bgcolor
		self.title_color = title_color
		self.icon_color = icon_color
		self.center_title = center_title
		self.on_click_btn = on_click_btn
		self.btn_icon = btn_icon
		
		self.update()
	
	def update (self):
		v = self.__self_ui
		l = self.__title_label
		b = self.__bar_btn
		
		if self.page == None: return

		if self.bgcolor == None:
			v.bgcolor = self.page.bgcolor
		else:
			v.bgcolor = self.bgcolor
		
		l.value = self.title
		l.color = self.title_color

		if self.center_title:
			v.title = None
			v.center_title = l
		else:
			v.title = l
			v.center_title = None
		
		b.width = 35
		b.action = self.__custom_bar_action
		b.icon_color = self.icon_color
		b.height = 35

		if v.page == None: return
		v.update()
	
	
	def __custom_bar_action (self, *args):
		do_action(self.on_click_btn, [])
	
	
	@property
	def self_ui (self):
		return self.__self_ui
