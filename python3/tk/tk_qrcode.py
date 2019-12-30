from tkinter import *
from .tk_widget import TKWidget
from utils.config import config
from PIL import Image, ImageTk
import qrcode

class TKQRCode(TKWidget):

	def __init__(self,parent,l=0, t=0, w=280, h=240, show=False):

		TKWidget.__init__(self, parent)

		self.image = None

		# main frame
		self.frame = Frame(parent.frame, background="white", borderwidth=0, relief="solid")
		self.place_widget(self.frame,l, t, w, h, show)

		self.label = Label(self.frame)
		self.place_widget(self.label,20, 0, 240, 240)

		self.label['bg'] = self.frame['bg']


	def generate(self, data):

		qr = qrcode.QRCode(
			version=None,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=3,
			border=4,
		)
		qr.add_data(data)
		qr.make(fit=True)

		image = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
		image = image.resize((240, 240),Image.ANTIALIAS)

		photo = ImageTk.PhotoImage(image)
		self.label.config(image=photo)
		self.label.saveicon = self.label   # otherwise it disappears
		self.label.savephoto = photo

	def destroy(self):
		#self.hide_widget(self.label)
		#self.label.saveicon = None
		#self.label.savephoto = None
		#self.label = None
		self.hide()

	def register_click(self, callback):

		# overloaded TKWidget because we need to respond if child windows are clicked as well
		self.frame.bind("<Button-1>",callback)
		self.label.bind("<Button-1>",callback)



