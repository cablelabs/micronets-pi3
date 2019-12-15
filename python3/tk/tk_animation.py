import os, sys, time
import threading
from threading import Timer
import PIL.Image
import PIL.ImageTk

from tkinter import *
from .tk_widget import TKWidget

from utils.syslogger import SysLogger

# Logfile is /tmp/<argv[0]>.log
logger = SysLogger().logger()

frame_interval = .05

class TKAnimation(TKWidget):

	def __init__(self,parent, filename, duration, callback=None, preload=True, l=0, t=40, w=280, h=160, show=False):

		TKWidget.__init__(self)

		self.parent = parent

		# For this widget, we want a backing frame with a black background to eliminate any flicker
		self.frame = Frame(parent.frame, bg='black')
		self.place_widget(self.frame, l, t, w, h, show)

		# The surface that the animation frames are rendered on. The parent is the backing frame
		self.image = Label(self.frame)
		self.image.place( x=0, y=0, width=w, height=h)
		self.image['bg'] = self.frame['bg']

		self.frames = []
		self.frames_loaded = 0
		self.duration = duration
		self.filename = filename
		self.callback = callback
		self.loading = False
		self.cancel_animation = False
		self.frame_count = int(duration / frame_interval)
		self.can_unload = True

		if preload:
			thr = threading.Thread(target=self.load_frames, args=()).start()

	def load_frames(self):

		self.loading = True

		file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../images', self.filename))

		gif = PIL.Image.open(file_path, mode='r')
		self.frames = []

		if gif:

			if self.duration > 0:
				max_frames = self.frame_count
			else:
				max_frames = sys.maxint

			# load up to frame_count frames, file may be shorter.
			try:
				self.frames_loaded = 0
				while self.frames_loaded < max_frames:
					self.frames.append(gif.copy())
					self.frames_loaded += 1
					gif.seek(self.frames_loaded)
			except EOFError:
				pass

			except:
				print("Error processing animated gif file: ", self.filename, " - ", sys.exc_info()[0])
				raise

			finally:
				self.loading = False
				gif.close()
		else:
			loading = False

	def unload(self):
		self.frames = []
		self.frames_loaded = 0
		self.frame_count = 0
		self.loading = False
		self.cancel_animation = False
		self.image.save = None

	def cancel(self):
		self.cancel_animation = True

	def animate(self):
		self.cancel_animation = False

		# if we preloaded, ensure it has finished
		while self.loading:
			time.sleep(frame_interval)

		# if we didn't preload, load synchronously now
		if self.frames_loaded == 0:
			self.load_frames()

		i = 0
		while i <= self.frame_count:

			max_frames = self.frames_loaded	# avoid race condition with unload
			if max_frames:
				index = i % max_frames
				photo = PIL.ImageTk.PhotoImage(self.frames[index])
				self.image.config(image=photo)
				self.image.save = photo # prevent from being garbage collected while active
				time.sleep(frame_interval)
				i += 1
				if self.cancel_animation and self.callback:
					self.callback(True)
					self.hide()
					return

		if self.callback:
			self.callback(False)
			self.hide()

	def start(self):
		thr = threading.Thread(target=self.animate, args=()).start()
		self.show()		
		pass

	def stop(self):
		self.cancel_animation = False

	



	'''
# animate frames
	i = 0
	ethernet_displayed = False
	#ethernet_displayed = True

	wifi_ssid = None
	wifi_ip = None

	while i <= frame_count:
		index = i % len(frames)
		photo = PIL.ImageTk.PhotoImage(frames[index])
		splash_image.config(image=photo)
		splash_image.image = photo # prevent from being garbage collected while active
		time.sleep(frame_interval)
		i += 1
		#header.config(text=str(i))

		# display ethernet address when starting up, if connected.
		if not ethernet_displayed:
			ethernet_ip = get_ethernet_ipaddress()
			if (ethernet_ip):
				footer.config(text="ETH: "+ ethernet_ip)
				ethernet_displayed = True

		# check for wifi connected
		if not wifi_ssid:
			wifi_ssid = get_ssid()
		elif not wifi_ip:
			wifi_ip = get_wifi_ipaddress()
		else:
			# we're connected and online.
			if i > min_frame_count:
				# end animation
				frame_count = 0
				display_demo_status()
				add_connected_messages()

		if i == frame_count:
			# end of animation and not connected
			if not has_network():
				add_message("Not provisioned.")                
			elif not get_ssid():
				clear_messages()
				add_message("Not associated:")
				stanza = get_network_stanza()
				for line in stanza:
					line = line.replace("\n", "").replace("\t","  ")
					if len(line) > 35:
						line = line[:35]+'...'
					add_message(line)
			else:
				add_message("Associated: "+ get_ssid())
				if not get_wifi_ipaddress():
					add_message("No IP address")
			display_demo_status()

	# clean up
	photo = None
















	def animate_fireworks():

	global demo_ssid, demo_wifi_ip

	file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'fireworks320-01.gif'))

	gif = PIL.Image.open(file_path, 'r')
	frames = []

	frame_interval = .05
	fireworks_duration = config.get('onboardAnimationSeconds', 5)
	frame_count = int(fireworks_duration / frame_interval)

	try:
		i = 0
		while i < frame_count:
			i += 1
			frames.append(gif.copy())
			gif.seek(len(frames))
	except EOFError:
		pass

	# prepare frame to receive images
	fireworks_image = Label(window, bg = 'black')
	place_widget(fireworks_image,0, banner_h, main_w, main_h)
	fireworks_image['bg'] = demo_frame['bg']
	show_widget(demo_frame)
	
	# allow canceling of the animation by touching the image
	fireworks_image.bind("<Button-1>", cancel_fireworks)

	hide_widget(splash_frame)
	# animate frames
	frame_count = len(frames)
	i = 0
	while i < frame_count:
	#for frame in frames:
		frame = frames[i]
		photo = PIL.ImageTk.PhotoImage(frame)
		fireworks_image.config(image=photo)
		fireworks_image.image = photo # prevent from being garbage collected while active
		time.sleep(frame_interval)
		i += 1

	# clean up
	photo = None

	hide_widget(fireworks_image)
	#hide_widget(demo_frame)

	if fireworks_image:
		fireworks_image.config(image=None)
		fireworks_image.image = None
		fireworks_image['bg'] = None


	add_connected_messages()
	display_demo_status()


def display_fireworks():
	add_message("start fireworks")
	thr = threading.Thread(target=animate_fireworks, args=()).start()

	'''