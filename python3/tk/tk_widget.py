
# Base class for all of our UI elements
from tkinter import *

# !! This requires a symlink utils -> ../utils, python 2.7 cannot do sibling folder imports. 
from utils.syslogger import SysLogger
logger = SysLogger().logger()

import os, sys
#import PIL.Image
#import PIL.ImageTk

class Placement:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

# base class for high level widgets
class TKWidget():
	font1=("HelveticaNeue-Light", 20, 'normal')
	font2=("HelveticaNeue-Light", 16, 'normal')
	font3=("HelveticaNeue-Light", 12, 'normal')
	font4=("HelveticaNeue-Light", 18, 'normal')
	font5=("HelveticaNeue-Light", 8, 'normal')

	def __init__(self):
		self.frame = None
		self.placements = {} # position/size of self and all children

	def place_widget(self, widget, layout, show=True):
		self.place_widget(layout.l, layout.t, layout.w, layout.h, show)

	def place_widget(self, widget, l, t, w, h, show=True):
		self.placements[widget] = Placement(l, t, w, h)
		if show:
			self.show_widget(widget)

	def show_widget(self, widget):
		p = self.placements[widget]
		widget.place(x=p.x, y=p.y, width=p.width, height=p.height)

	def hide_widget(self, widget):
		widget.place_forget()

	def show(self):
		if not self.frame.winfo_ismapped():
			self.show_widget(self.frame)

	def hide(self):
		if self.frame.winfo_ismapped():
			self.hide_widget(self.frame)

	'''
	def add_icon(self, imagename, x, y, width, height, show=True):
		path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../images', imagename))
		img = PIL.Image.open(path)
		img = img.resize((width, height),PIL.Image.ANTIALIAS)
		icon = PIL.ImageTk.PhotoImage(img)
		iconFrame = Label(self.frame, image=icon)
		self.place_widget(iconFrame, x, y, width, height, show)
		iconFrame['bg'] = self.frame['bg']
		iconFrame.saveicon = icon   # otherwise it disappears
		return iconFrame
	'''
	def register_click(self, callback):
		self.frame.bind("<Button-1>",callback)

	def register_click_release(self, callback):
		self.frame.bind("<ButtonRelease-1>",callback)

	'''
	def add_button(self, l, t, w, h, imagename, callback, callback2=None, show=True):
		logger.info("add_button (top): "+str(t))
		image = None
		icon = None
		if imagename != None:
			icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../images', imagename))
			img = PIL.Image.open(icon_path)
			img = img.resize((w,h),PIL.Image.ANTIALIAS)
			icon = PIL.ImageTk.PhotoImage(img)
			button = Label(self.frame, image=icon)
		else:
			button = Label(self.frame)

		button.bind("<Button-1>",callback)
		if callback2 != None:
			button.bind("<ButtonRelease-1>",callback2)

		self.place_widget(button, l, t, w, h, show)
		button['bg'] = self.frame['bg']
		button.saveicon = icon   # otherwise it disappears
		return button
	'''