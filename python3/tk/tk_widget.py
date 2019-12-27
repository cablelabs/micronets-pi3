# Base class for all of our UI elements
from tkinter import *
import os, sys

# Logfile is /tmp/<argv[0]>.log
from utils.syslogger import SysLogger
logger = SysLogger().logger()


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

	def __init__(self, parent):
		self.parent = parent
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

	def register_click(self, callback):
		self.frame.bind("<Button-1>",callback)

	def register_click_release(self, callback):
		self.frame.bind("<ButtonRelease-1>",callback)
