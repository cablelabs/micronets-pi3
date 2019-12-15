# Button panel on right side. Mirrors hardware buttons.
# 0: Onboard
# 1: Cycle Wifi
# 2: Settings
# 3: Power/Reload

from tkinter import *
from .tk_widget import TKWidget
from .tk_button import TKButton

# square icons
icon_size = 36
frame_size = 40
margin = (frame_size - icon_size) / 2
max_buttons = 4

class TKButtons(TKWidget):

	def __init__(self,parent,l=280, t=40, w=40, h=160, show=True):

		TKWidget.__init__(self)

		self.button_onboard = 0
		self.button_cycle = 1
		self.button_settings = 2
		self.button_power = 3
		self.top = t
		self.left = l
		self.width = w
		self.height = h
		self.buttons = [None, None, None, None]

		self.parent = parent

		# main frame
		self.frame = Label(parent.frame, fg="white", bg="gray80")
		#self.place_widget(self.frame,layout, show)
		self.place_widget(self.frame,l, t, w, h, show)

	def add_button(self, index, imagename, callback, callback2=None, show=True):
		if index >= max_buttons:
			return None

		top = (index * frame_size) + margin

		button = TKButton(self, margin, top, icon_size, icon_size, imagename, callback, callback2, show)
		self.buttons[index] = button

		return button

