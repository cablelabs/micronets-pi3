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

	def __init__(self,parent, filename, duration, callback=None, preload=True, l=0, t=40, w=280, h=160, cancel_tap=True, show=False):

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
		# TODO: allow for playing the whole animation. Pass 0 duration??
		self.frame_count = int(duration / frame_interval)


		# tap to cancel animation
		if cancel_tap:
			self.image.bind("<Button-1>",self.cancel)


		if preload:
			self.preload()

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

	def preload(self):
		thr = threading.Thread(target=self.load_frames, args=()).start()

	def unload(self):
		self.frames = []
		self.frames_loaded = 0
		self.frame_count = 0
		self.loading = False
		self.image.save = None

	def start(self):
		thr = threading.Thread(target=self.animate, args=()).start()
		self.show()		
		pass

	def cancel(self, null_arg=0):
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
		while i <= self.frame_count and not self.cancel_animation:

			max_frames = self.frames_loaded	# avoid race condition with unload
			if max_frames:
				index = i % max_frames
				photo = PIL.ImageTk.PhotoImage(self.frames[index])
				self.image.config(image=photo)
				self.image.save = photo # prevent from being garbage collected while active
				time.sleep(frame_interval)
				i += 1

		if self.callback:
			logger.info("animation " + "completed" if self.cancel_animation else "canceled")
			self.callback(self.cancel_animation)
			self.hide()

