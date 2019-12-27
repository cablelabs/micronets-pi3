#!/usr/bin/env python3
# onboard functionality for clinic demo

import os, sys, time, traceback
import json
import requests
import base64

from utils.syslogger import SysLogger
from utils.config import config
import threading
from threading import Timer

import utils.wpa_cli as wpa_cli
import utils.network as network
from utils.ecc_keys import ecc_keys

# Logfile is /tmp/<argv[0]>.log
logger = SysLogger().logger()

# Subscriber certs directory
folder = os.path.dirname(os.path.realpath(__file__))
certs_dir = os.path.join(folder, '../certs')

# Required by cancel and submit_csr
deviceID = None

# wrap called function in try/except. All functions require callback as first arg
def __run_wrapper__( func, callback, *args):
	try:
		func(callback, *args)
	except Exception as e:
		logger.error("** "+ func.__name__ + " **" )
		logger.error(e.__doc__)
		logger.error(e.message)
		logger.error('-'*60)
		logger.error(traceback.print_exc())
		logger.error('-'*60)
		callback(e.message)

# Entry points
def start(callback, messages):
	thr = threading.Thread(target=__run_wrapper__, args=(__start__, callback, messages,)).start()

def cancel(callback, messages):
	thr = threading.Thread(target=__run_wrapper__, args=(__cancel__, callback, messages,)).start()

# Async methods
def __start__(callback, messages):

	# Read device profile
	device = load_device()

	# Advertise
	csrt = advertise(device, callback, messages)
	if csrt:
		# Submit CSR Request
		credentials = submit_csr(csrt, callback, messages)
		if credentials:
			# Save Credentials
			if save_credentials(credentials, callback, messages):
				# Restart Wifi
				wpa_cli.reconfigure()
				callback(None)

def __cancel__(callback, messages):
	headers = {'content-type': 'application/json'}
	body = {'deviceID': deviceID}
	data = json.dumps(body)
	url = make_url('device/v1/cancel')
	response = requests.post(url, data = data, headers = headers)
	logger.info("response received from device/v1/cancel")
	messages.add_message("Canceled Onboard: {}".format(response.status_code))
	callback(None)

# Load device profile
def load_device():
	profile = config.get("deviceProfile")
	folder = os.path.dirname(os.path.realpath(__file__))
	filename = os.path.join(folder, '../config/devices/'+profile+'.json')

	try:
		with open(filename, 'r') as infile:  
			file_data = infile.read()
			device = json.loads(file_data)

	except (OSError, IOError, KeyError) as e: # FileNotFoundError does not exist on Python < 3.3
		logger.info("Unable to load device profile: "+filename)
		device = { "vendor": "XYZ", "type": "ABCD","model": "1234","class": "Generic","deviceConnection": "wifi", "deviceName": "Default Device", "modelUID64" : "LMNOP12345"}
		pass

	device['deviceID'] = ecc_keys.public_key_hash()
	device['macAddress'] = network.get_mac()
	device['serial'] = device['vendor'][:1] + device['model'][:1] + '-' + device['deviceID'][-8:].upper()

	return device

# Advertise the device on the registration server
def advertise(device, callback, messages):

	# Save in case we cancel
	global deviceID
	deviceID = device['deviceID']

	data = json.dumps(device)
	logger.info("advertising device:\n{}".format(data))
	messages.add_message("Advertise Device")

	headers = {'content-type': 'application/json'}
	url = make_url('device/v1/advertise')
	response = requests.post(url, data = data, headers = headers)

	if response.status_code == 204:
		callback("Onboard canceled")
		return None
	elif response.status_code != 200:
		callback("HTTP Error: {}".format(response.status_code))
		return None

	return response.json()

# Submit the CSR
def submit_csr(csrt, callback, messages):

	# Create the submit message
	reqBody = {'deviceID': deviceID}

	# Generate a CSR
	ecc_keys.generate_csr("wifi_csr")
	reqBody['csr'] = ecc_keys.encoded_csr_base64()

	data = json.dumps(reqBody)
	
	logger.info("submitting CSR")
	display.add_message("Submitting CSR")

	# Sleeps are for demo visual effect. Can be removed.
	time.sleep(2)

	headers = {'content-type': 'application/json','authorization': csrt['token']}
	url = make_url('device/v1/cert')
	response = requests.post(url, data=data, headers=headers)
	if response.status_code != 200:
		callback("submit_csr - HTTP Error: {}".format(response.http_status))
		return None

	# Parse out reply and set up wpa configuration
	credentials = response.json()
	logger.info(credentials)

	return credentials

def save_credentials(credentials, callback, messages):

	ssid = credentials['subscriber']['ssid']
	wifi_cert64 = credentials['wifiCert']
	ca_cert64 = credentials['caCert']

	wifi_cert = base64.b64decode(wifi_cert64);
	ca_cert = base64.b64decode(ca_cert64);

	logger.info("ssid: {}".format(ssid))
	logger.info("wifi_cert: {}".format(wifi_cert))
	logger.info("ca_cert: {}".format(ca_cert))

	if hasattr(credentials, 'passphrase'):
		passphrase = credentials['passphrase']
	else:
		passphrase = "whatever"

	# remove network if it exists
	wpa_cli.remove_networks(ssid)

	identity = 'micronets'

	# generate configuration
	network = {}
	network['ssid'] = '"' + ssid + '"'
	network['scan_ssid'] = '1'
	network['key_mgmt'] = 'WPA-EAP'
	network['group'] = 'CCMP TKIP'
	network['eap'] = 'TLS'
	network['identity'] = '"' + identity + '"'
	network['ca_cert'] = '"' + certs_dir + '/ca.pem' + '"'
	network['client_cert'] = '"' + certs_dir + '/wifi.crt' + '"'
	network['private_key'] = '"' + certs_dir + '/wifi.crt' + '"'
	network['private_key_passwd'] = '"' + passphrase + '"'
	network['priority'] = '10'

	# Save keys and certs
	with open(certs_dir + '/ca.pem', 'wb') as f:
		f.write(ca_cert)
	with open(certs_dir + '/wifi.crt', 'wb') as f:
		f.write(wifi_cert)

	# add subscriber network
	wpa_cli.add_network(network)

	return True

def make_url(path):
	base_url = config.get("registrationServer")
	url = "{}/{}".format(base_url, path)
	return url

def reset_device():
	pass

if __name__ == '__main__':

	class Messages():

		def add_message(self, msg):
			print("MSG: {}".format(msg))

	messages = Messages()

	def callback(info):
		print("callback: {}".format(info))

	if len(sys.argv) > 1 and sys.argv[1] == 'reset':
		logger.info("reset")
		reset_device()
	else:
		logger.info("Onboarding")
		newKey = len(sys.argv) > 1 and sys.argv[1] == 'newkey'
		start(callback, messages)
