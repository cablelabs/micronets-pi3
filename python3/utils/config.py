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

    def load_config(self):
        try:
            with open(filename, 'r') as infile:  
                file_data = infile.read()
                self.config = json.loads(file_data)

                logger.info("config loaded OK: "+str(len(self.config))+ " keys")
                #logger.info("\n" + json.dumps(config))

        except (OSError, IOError, KeyError, FileNotFoundError) as e:
            logger.info("config load error: "+e)
            pass

    def dump(self, file=None):
        if not file:
            return json.dumps(self.config,  sort_keys=True, indent=4, separators=(',', ': '))
        else:
            with open(file, 'w') as outfile:  
                json.dump(self.config, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    # get/set methods are recursive
    def set(self, key, value, dictionary=None):

        if not dictionary:
            dictionary = self.config

        if isinstance(key, list):
            # array of keys
            k0 = key.pop(0)
            if not k0 in dictionary:
                # This is an insert
                if len(key) == 0:
                    # no more keys, insert value
                    dictionary[k0] = value
                else:
                    dictionary[k0] = {}
                    self.set(key, value, dictionary[k0])
            else:
                # This is an update
                x = dictionary[k0]
                if isinstance(x, dict):
                    self.set(key, value, x)
                else:
                    dictionary[k0] = value
        else:
            # single key, update or insert
            dictionary[key] = value

    def get(self, key, default=None, dictionary=None):

        if not dictionary:
            dictionary = self.config

        if isinstance(key, list):
            # array of keys
            k0 = key.pop(0)
            if k0 in dictionary:
                x = dictionary[k0]
                if isinstance(x, dict):
                    return self.get(key, default, x)
                else:
                    return x
            else:
                return default if default else None
        else:
            # single key
            if key in dictionary:
                return dictionary[key]
            else:
                return default if default else None

# The one and only thing that gets imported with "from utils.config import *"
config = Config()
        
if __name__ == '__main__':

    # !!! You MUST run this from the parent directory: python3 -m utils.config
    # !!! - note the -m switch and no .py extension

    _config = Config()

    # initial values
    logger.info("countdown: "+str(_config.get('countdown')))
    logger.info("[dppProxy][password]: "+str(_config.get(['dppProxy','password'])))

    # update
    _config.set("countdown", 809)
    _config.set(['dppProxy','password'], 'flerb')

    # modified values
    logger.info("countdown: "+str(_config.get('countdown')))
    logger.info("[dppProxy][password]: "+str(_config.get(['dppProxy','password'])))

    # fetch non-existent
    logger.info("aaa: "+str(_config.get('aaa')))
    logger.info("[bbb][ccc]: "+str(_config.get(['bbb','ccc'])))

    # fetch non-existent with defaults
    logger.info("aaa: "+str(_config.get('aaa', 'xyz')))
    logger.info("[bbb][ccc]: "+str(_config.get(['bbb','ccc'], 'tbd')))

    # insert new key value pairs
    _config.set("aaa", 888)
    _config.set(['bbb','ccc'], 'grimp')

    # fetch inserted values
    logger.info("aaa: "+str(_config.get('aaa')))
    logger.info("[bbb][ccc]: "+str(_config.get(['bbb','ccc'])))

    # dump JSON
    _config.dump(os.getenv("HOME")+"/dump.json")
    logger.info(_config.dump())

    logger.info("comcast: "+str(_config.get("comcast")))

    logger.info(_config.get(['dppProxy','msoPortalUrl']))


