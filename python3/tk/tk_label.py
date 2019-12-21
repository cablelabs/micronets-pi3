import os
from tkinter import *
from .tk_widget import TKWidget

class TKLabel(TKWidget):

	def __init__(self,parent,l, t, w, h, text, fg='white', font=TKWidget.font2, bg = None, show=True):

		TKWidget.__init__(self, parent)

		self.frame = Label(parent.frame, text=text, fg=fg, font=font)
		self.place_widget(self.frame, l, t, w, h, show)

		if bg:
			self.frame.config(bg=bg)
		else:
			self.frame['bg'] = parent.frame['bg']

	def clear(self):
		self.frame.config(text="")

	def set_font(self, font):
		self.frame.config(font=font)

	def set_color(self, color):
		self.frame.config(fg=color)

	def set_text(self, text, color=None, font=None):
		if color:
			self.frame.config(fg=color)
		if font:
			self.frame.config(font=font)

		self.frame.config(text=text)
