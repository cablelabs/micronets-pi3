import os
from tkinter import *
from .tk_widget import TKWidget
from PIL import Image
from PIL import ImageTk

class TKIcon(TKWidget):

	def __init__(self,parent,l, t, w, h, imagename,show=True):

		TKWidget.__init__(self)

		self.parent = parent

		image = None
		icon = None

		icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../images', imagename))


		img = Image.open(icon_path)
		img = img.resize((w,h),Image.ANTIALIAS)
		icon = ImageTk.PhotoImage(img)
		self.frame = Label(parent.frame, image=icon)

		self.place_widget(self.frame, l, t, w, h, show)
		self.frame['bg'] = parent.frame['bg']
		self.frame.saveicon = icon   # otherwise it disappears
