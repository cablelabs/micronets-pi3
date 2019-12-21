from tkinter import *
from .tk_widget import TKWidget
from .tk_icon import TKIcon
from utils.config import config

class TKHeader(TKWidget):

	def __init__(self, parent, mode, title, font, l=0, t=0, w=320, h=40, show=True):

		TKWidget.__init__(self, parent)

		if mode == 'dpp':
			bg = "DodgerBlue4"
			icon = 'dpp.png'
		else:
			bg = 'teal'
			icon = 'clinic.png'


		# main frame
		self.frame = Label(parent.frame, text=title, fg="white", font=font, bg=bg)
		self.place_widget(self.frame,l, t, w, h, show)

		# mode icon
		self.mode_icon = TKIcon(self, 4, 2, 36, 36, icon)

	def clear(self):
		self.frame.config(text=title)
		self.hide_widget(self.mode_icon)

	def set_title(title):
		self.frame.config(text=title)
