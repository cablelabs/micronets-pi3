# base class for proto-pi apps

import os, sys, time
import datetime
import threading
from threading import Timer
from tkinter import *
from .tk_main import TKMain
from utils.config import config
import pyscreenshot as ImageGrab
import utils.globals as globals
import utils.wpa_cli as wpa_cli

# This will generate a key pair if one does not exist
from utils.ecc_keys import ecc_keys

from utils.syslogger import SysLogger
logger = SysLogger().logger()

import RPi.GPIO as GPIO

class TKApp():

	def __init__(self):

		globals.app = self
		self.frame = None

		self.window = Tk()

		screen_width = self.window.winfo_screenwidth()
		screen_height = self.window.winfo_screenheight()

		logger.info("Screen: "+str(screen_width) + " x " + str(screen_height))

		self.main_x = 0
		self.main_y = 0

		if screen_width >= 640 and screen_height >= 480:
			# External monitor/VNC
			self.main_x = 40
			self.main_y = 40
			self.hasTitleBar = True
		else:
			# hide title bar
			self.hasTitleBar = False
			self.window.overrideredirect(1)


		self.window.geometry("320x240+" + str(self.main_x) + "+" +str(self.main_y))

		# Empty main window
		self.main_window = TKMain(self.window, 0, 0, 320, 240, True)

		# GPIO
		GPIO.setwarnings(False)
		# Board layout (pins)
		GPIO.setmode(GPIO.BCM)

		# PiTFT buttons
		GPIO.setup([17, 22, 23, 27], GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# Backlight PWM
		GPIO.setup(18, GPIO.OUT)
		self.backlightOn = True
		self.backlight = GPIO.PWM(18, 1000)
		self.backlight.start(100)

		# Temp for development, using VNC and don't need screen on
		#self.toggle_backlight()

		# Overload in derived classes
		self.dispatch = {}
		self.visible_windows = {}
		self.visible_buttons = {}
		self.base_windows = []
		self.all_windows = []
		self.standard_buttons = []
		self.all_buttons = []


	def run(self):

		# delay exit until application established
		def enableExit():
			self.canExit  = True

		threading.Timer(10.0, enableExit).start()

		self.window.mainloop()

		#while 1:
		#	self.window.update()
		#	time.sleep(0.01)


	# These are used to register Tkinter controls that are not subclassed from TKWidget
	def register_click(self, control, callback):
		control.bind("<Button-1>",callback)

	def register_click_release(self, control, callback):
		control.bind("<ButtonRelease-1>",callback)


	# common functions for all proto applications

	# Update user interface for new state and initialize as required
	def set_state(self, new_state):

		self.last_state = self.state
		self.state = new_state

		# Hide/show windows
		self.place_widgets(self.all_windows, self.visible_windows[new_state])

		# Hide/show buttons
		self.place_widgets(self.all_buttons, self.visible_buttons[new_state])

		# Do any required cleanup from old state
		if self.last_state and self.dispatch[self.last_state][1]:
			self.dispatch[self.last_state][1]()

		# Do any required initialization for new state
		if self.dispatch[new_state][0]:
			self.dispatch[new_state][0]()

		self.state = new_state

	# Hide/show widgets for the new state
	def place_widgets(self, all_widgets, visible_widgets):
		for widget in all_widgets:
			if widget in visible_widgets:
				widget.show()
			else:
				widget.hide()

	def take_screenshot(self, null_arg=0):

		# Screenshots directory
		screenshots_folder = '/etc/micronets/screenshots'
		if not os.path.exists(screenshots_folder):
			os.makedirs(screenshots_folder)

		# Filename
		filename = str(datetime.datetime.now()).split('.')[0].replace(':','.')+".jpg"
		filepath = screenshots_folder + "/" + filename

		if self.hasTitleBar:
			screenshot = ImageGrab.grab(bbox=(self.main_x+2, self.main_y+30, self.main_x+320+2, self.main_y+240+30))
		else:
			screenshot = ImageGrab.grab(bbox=(self.main_x, self.main_y, self.main_x+320, self.main_y+240))

		screenshot.save(filepath)

	def restart(self):
		os.popen("sudo systemctl restart lightdm")

	def reboot(self):
		os.popen("sudo reboot now")

	def shutdown(self):
		os.popen("sudo shutdown -h now")


	# event handler to toggle the TFT backlight
	def toggle_backlight(self, null_arg=0):
		if self.backlightOn:
			self.backlightOn = False
			self.backlight.start(0)
		else:
			self.backlightOn = True
			self.backlight.start(100)


if __name__ == '__main__':
    app = TKApp()
    app.run()

