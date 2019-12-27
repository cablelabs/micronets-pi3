from tkinter import *

from .tk_widget import TKWidget
from .tk_icon import TKIcon
from .tk_label import TKLabel

import utils.wpa_cli as wpa_cli
import utils.globals as globals
import utils.network as network
from utils.config import config

from utils.syslogger import SysLogger

# Logfile is /tmp/<argv[0]>.log
logger = SysLogger().logger()

class TKStatus(TKWidget):

	def __init__(self,parent,l=0, t=40, w=280, h=160, show=True):

		TKWidget.__init__(self, parent)

		# main frame
		self.frame = Frame(parent.frame, background="white", borderwidth=0, relief="solid")
		self.place_widget(self.frame,l, t, w, h, show)

		# center of frame
		l = (w - 64) / 2
		t = (h - 64) / 2

		# Status icons
		self.connected_icon = TKIcon(self, l, t, 64, 64, 'green-check.png', False)
		self.not_connected_icon = TKIcon(self, l, t, 64, 64, 'no-connection.png', False)

		# SSID label
		self.ssid_label = TKLabel(self, 4, t+64+10, w-8, 24, "NOT CONNECTED", "DodgerBlue4", TKWidget.font3)

	def clear(self):
		self.connected_icon.hide()
		self.not_connected_icon.hide()
		self.ssid_label.set_text("")

	def set_connected(self, connected):
		if connected:
			self.connected_icon.show()
			self.not_connected_icon.hide()
		else:
			self.connected_icon.hide()
			self.not_connected_icon.show()

	# only change text if status changed (avoid flicker)
	def set_ssid_text(self, text):
		if self.ssid_label.frame.cget("text") != text:
			self.ssid_label.set_text(text)

	def update(self):

		ssid = network.get_ssid()
		wifi_ip = network.get_wifi_ipaddress()

		if config.get('mode') == 'dpp':
			is_provisioned = wpa_cli.has_network()
		else:
			is_provisioned = wpa_cli.get_provisioned() != None

		if is_provisioned and ssid:
			if not globals.sparse_mode:
				self.set_ssid_text(ssid)
			else:
				self.set_ssid_text("CONNECTED")
				
			if wifi_ip:
				self.set_connected(True)
			else:
				self.set_connected(False)
		else:
			self.set_connected(False)

			if is_provisioned:
				self.set_ssid_text("NOT CONNECTED")
			else:
				if globals.sparse_mode:
					self.set_ssid_text("NOT CONNECTED")
				else:
					self.set_ssid_text("NOT PROVISIONED")

	def register_click(self, callback):

		# overloaded TKWidget because we need to respond if child windows are clicked as well
		self.frame.bind("<Button-1>",callback)
		self.connected_icon.frame.bind("<Button-1>",callback)
		self.not_connected_icon.frame.bind("<Button-1>",callback)
		self.ssid_label.frame.bind("<Button-1>",callback)







