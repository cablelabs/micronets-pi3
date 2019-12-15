import os
from tkinter import *
from .tk_widget import TKWidget
from PIL import Image
from PIL import ImageTk

#from utils.config import * 

class TKButton(TKWidget):

	def __init__(self,parent,l, t, w, h, imagename, callback=None, callback2=None,show=True):

		TKWidget.__init__(self)

		self.parent = parent

		image = None
		icon = None

		if imagename != None:
			icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../images', imagename))
			img = Image.open(icon_path)
			img = img.resize((w,h),Image.ANTIALIAS)
			icon = ImageTk.PhotoImage(img)
			self.frame = Label(parent.frame, image=icon)
		else:
			self.frame = Label(parent.frame, fg='white')

		if callback != None:
			self.frame.bind("<Button-1>",callback)
		if callback2 != None:
			self.frame.bind("<ButtonRelease-1>",callback2)

		self.place_widget(self.frame, l, t, w, h, show)
		self.frame['bg'] = parent.frame['bg']
		self.frame.saveicon = icon   # otherwise it disappears

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
