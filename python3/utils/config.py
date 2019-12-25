import os
import json
from .syslogger import SysLogger

__all__ = ["config"]

# Logfile is /tmp/protodpp.log
logger = SysLogger().logger()

folder = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(folder, '../../config/config.json')

class Config():

	def __init__(self):

		self.load_config()
		self.set_defaults()
		self.save_config()

	def config_default(self, key, default):

		if not self.get(key):
			self.set(key, default)

	def save_config(self):
		#with open(filename, 'w') as outfile:  
		#    json.dump(self.config, outfile, sort_keys=True, indent=4, separators=(',', ': '))
		self.dump(filename)

	def set_defaults(self):
		# config defaults
		self.config_default('mode', 'dpp')
		self.config_default('splashAnimationSeconds', 10)
		self.config_default('onboardAnimationSeconds', 5)
		self.config_default('messageTimeoutSeconds', 45)

		# clinic mode specific
		self.config_default('registration_server', 'https://alpineseniorcare.com/micronets')
		self.config_default('device_profile', 'device-0')

		# dpp mode specific
		self.config_default('vendorCode', "DAWG")
		self.config_default('channel', 1)
		self.config_default('channelClass', 81)
		self.config_default('qrcode_countdown', 30)
		# proxy settings are used when simulating the iphone mobile application (click on qrcode)
		self.config_default(['dppProxy','msoPortalUrl'], "https://mso-portal-api.micronets.in")
		self.config_default(['dppProxy','username'], "grandma")
		self.config_default(['dppProxy','password'], "grandma")
		self.config_default(['dppProxy','deviceModelUID'], "AgoNDQcDDgg")

		# customization flags
		self.config_default('demo', True)
		self.config_default('comcast', False)

	def reset(self):
		self.config = {}

	def load_config(self):
		try:
			with open(filename, 'r') as infile:  
				file_data = infile.read()
				self.config = json.loads(file_data)

				logger.info("config loaded OK: "+str(len(self.config))+ " keys")
				#logger.info("\n" + json.dumps(config))

		except (KeyError, FileNotFoundError) as e:
			logger.info("load_config: config file does not exist. Default will be generated")

			# Start empty, create boilerplate from defaults.
			self.config = {}
			pass

	def dump(self, file=None):
		if not file:
			return json.dumps(self.config,  sort_keys=True, indent=4, separators=(',', ': '))
		else:
			with open(file, 'w') as outfile:  
				json.dump(self.config, outfile, sort_keys=True, indent=4, separators=(',', ': '))

	def set(self, key, value):

		if isinstance(key, list):

			obj = self.config

			i = 0
			while i < (len(key)-1):
				k = key[i]
				if not k in obj or not isinstance(obj[k], dict):
					obj[k] = {}
				obj = obj[k]
				i += 1

			k = key[len(key)-1]
			obj[k] = value

		else:
			# single key, update or insert
			self.config[key] = value

	def get(self, key, default=None):
		if isinstance(key, list):
			obj = self.config
			i = 0
			while i < (len(key)-1):
				k = key[i]
				if not k in obj or not isinstance(obj[k], dict):
					return default if default else None
				obj = obj[k]
				i += 1

			k = key[len(key)-1]
			if k in obj:
				return obj[k]
			else:
				return default if default else None
		else:
			# single key
			if key in self.config:
				return self.config[key]
			else:
				return default if default else None

# The one and only thing that gets imported with "from utils.config import *"
config = Config()
		
if __name__ == '__main__':

	# !!! You MUST run this from the parent directory: python3 -m utils.config
	# !!! - note the -m switch and no .py extension
	# start empty
	config.reset()

	# initial values
	logger.info("countdown: "+str(config.get('countdown')))
	logger.info("[dppProxy][password]: "+str(config.get(['dppProxy','password'])))

	# update
	config.set("countdown", 809)
	config.set(['dppProxy','password'], 'flerb')

	# modified values
	logger.info("countdown: "+str(config.get('countdown')))
	logger.info("[dppProxy][password]: "+str(config.get(['dppProxy','password'])))

	# fetch non-existent
	logger.info("aaa: "+str(config.get('aaa')))
	logger.info("[bbb][ccc]: "+str(config.get(['bbb','ccc'])))

	# fetch non-existent with defaults
	logger.info("aaa: "+str(config.get('aaa', 'xyz')))
	logger.info("[bbb][ccc]: "+str(config.get(['bbb','ccc'], 'tbd')))

	# insert new key value pairs
	config.set("aaa", 888)
	config.set(['bbb','ccc'], 'grimp')

	# fetch inserted values
	logger.info("aaa: "+str(config.get('aaa')))
	logger.info("[bbb][ccc]: "+str(config.get(['bbb','ccc'])))

	# dump JSON
	config.dump("dump.json")
	logger.info(config.dump())



