from ..Tools.action import do_action
import flet
import time


class Navigate (object):
	def __init__ (self, page, controls, show=False, on_back=None, back_btn_color="#6da0ff"):
		if hasattr(page, "page"):
			raise NameError("The navigator accept only pages.")
		self.__page_controls = []
		for i in page.controls:
			self.__page_controls.append({"class":i, "props":dict(i.__dict__)})
		self.controls = controls
		self.__page = page
		self.__is_presented_ones = False
		self.swipe_back_started = False
		
		self.on_back = on_back
		
		self.backbtn = flet.TextButton(text="< Back", on_click=self.__custom_go_back)
		if page.appbar != None:
			pass
		
		if show:
			self.show()
	
	def show (self, *args):
		# reset
		self.__page.self_ui.appbar.actions.append(self.backbtn)
		self.__last_on_touch = self.__page.on_touch
		self.__page.on_touch = self.__on_swipe
		if self.__is_presented_ones == False:
			self.__page_controls = []
			for i in self.__page.controls:
				self.__page_controls.append({"class":i, "props":dict(i.__dict__)})
			self.__is_presented_ones = True
		# start showing	
		for i in self.__page_controls:
			i["class"].opacity = 0.0
		
		time.sleep(0.5)
		self.__page.clear()
		
		for i in self.controls:
			self.__page.add(i)
		
		self.__page.update()
	
	def back (self, *args):
		for i in self.__page.self_ui.appbar.actions:
			if type(i) == type(flet.TextButton()):
				self.__page.self_ui.appbar.actions.remove(i)
		self.__page.on_touch = self.__last_on_touch
		self.__page.clear()
		for i in self.__page_controls:
			self.__page.add(i["class"])
			i["class"].__dict__ = dict(i["props"])
		
		# do action
		do_action(self.on_back, [self])
		
		self.__is_presented_ones = True
		self.__page.update()
	
	def __on_swipe (self, state, cls):
		if state == "start" and int(cls.touch_x) < 35:
			self.swipe_back_started = True
		elif state == "move" and self.swipe_back_started:
			the_half_half_number_of_width = cls.width / 10
			if cls.touch_x >= the_half_half_number_of_width:
				self.swipe_back_started = False
				self.back()
			else:
				pass
		else:
			self.swipe_back_started = False
			self.__back_animator.width = 0
			
	
	def __custom_go_back (self, cls):
		self.back()
		do_action(self.back, [])
