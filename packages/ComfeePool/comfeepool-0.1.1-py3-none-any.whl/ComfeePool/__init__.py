# TheBlackmad
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import paho.mqtt.client as mqtt
import time
import threading
import logging
import sys
import json

from midea_inventor_lib import MideaClient 
from .ComfeeConfig import ComfeeConfig
from .ComfeeApplianceMapper import ComfeeApplianceMapper
from .ComfeeDehumidifierMapper import ComfeeDehumidifierMapper

from .const import (
	NAME,
	VERSION,
	POOLING_TIME
)

__version__ = VERSION


class ComfeePool():
	"""A class to manage a pool of Comfee smart devices and their MQTT integration.
    The integration comes in the form of /<level0>/<level1>/attribute"""

	def __init__(self, username:str='', password:str='', brokerIP:str = '127.0.0.1', brokerPort:int = 1883, 
				log_to_file: bool = False, log_file: str = "YeelightPool.log",
				debug: bool = False):
		"""Initialize the ComfeePool.

		Args:
		    brokerIP (str): IP address of the MQTT broker.
		    brokerPort (int): Port of the MQTT broker.
		    log_to_file (bool): Whether to log to a file.
		    log_file (str): Name of the log file.
		    debug (bool): Whether to enable debug-level logging.
		"""
		self.username = username
		self.password = password
		self.debug = debug
		self.log_to_file = log_to_file
		self.log_file = log_file
		self.stop_event = threading.Event()
        
		self.appliances = []
		self.MideaClient = None

		self.brokerIP = brokerIP
		self.brokerPort = brokerPort
		self.clientBroker = mqtt.Client()
				
		self._setup_logging()
		

	def _setup_logging(self):
		"""Sets up the logging configuration for the class."""
		if self.log_to_file:
			logging.basicConfig(filename=self.log_file, level=logging.DEBUG if self.debug else logging.INFO)
		else:
			logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if self.debug else logging.INFO)
			
			
	def connect(self):
		""" Establish connection to the MideaClient"""
		self.MideaClient = MideaClient(self.username, self.password, "")
		result = self.MideaClient.login()
		if result != 1:
			raise MideaPoolException(f"Error connecting to the MideaServer")
			
			
	def discover(self):
		""" Discover devices in the network."""
		appliances = self.MideaClient.listAppliances()
		if appliances == -1:
			raise Exception(f"Error discovering devices!")
		
		for appliance in appliances:
			self.MideaClient.get_device_status(appliance['id'])
			
			level0 = appliance['name']
			level1 = self.MideaClient.deviceStatus.__class__.__name__
			
			if level1=='MideaDehumidificationDevice':
				self.appliances.append(ComfeeDehumidifierMapper(appliance['id'], level0, level1))
			else:
				self.appliances.append(ComfeeApplianceMapper(appliance['id'], level0, level1))
				
			
	def start(self):
		"""Start the ComfeePool by connecting andn discovering devices."""		

		# Start MQTT loop in the background
		logging.info(f"Connecting to the broker on {self.brokerIP}:{self.brokerPort}")
		self.clientBroker.on_connect = self.on_connect
		self.clientBroker.on_message = self.on_message
		self.clientBroker.connect(self.brokerIP, self.brokerPort)
		self.clientBroker.loop_start()

		logging.info(f"Connecting to Midea . . .")
		self.connect()
		logging.info(f"Discovering devices in the network")
		self.discover()
		logging.info(f"Number of devices discovered: {len(self.appliances)}")
	
		try:		
			while not self.stop_event.is_set():

				for appliance in self.appliances:
					try:
						self.MideaClient.get_device_status(appliance.id)
						topics = appliance.mqttTopics_to_update(self.MideaClient.deviceStatus)
						
						for topic in topics:
							logging.info(f"Publishing {topic['topic']}, {topic['value']}")
							self.clientBroker.publish(topic['topic'], topic['value'])				
					except Exception as e:
						print(f"EXCEPTION: {e}")
				
				time.sleep(POOLING_TIME)
				
		except KeyboardInterrupt:
			self.stop()
		
		logging.info(f"Terminated ComfeePool")
		

	def stop(self):
		"""Stop the ComfeePool and gracefully shut down all threads."""
		logging.info("Stopping ComfeePool System...")
		self.stop_event.set()
		
				
	def on_connect(self, client, userdata, flags, rc):
		"""
		Callback for successful connection to the MQTT broker.

		:param client: The client instance for this callback.
		:param userdata: The private user data as set in Client() or userdata_set.
		:param flags: Response flags sent by the broker.
		:param rc: Connection result code.
		"""

		try:
			for appliance in self.appliances:
				command_topic = f"/{appliance.level0}/{appliance.level1}/command"
				client.subscribe(command_topic, 0)	# subscribe to all commands to this device
				logging.info(f"{appliance.id} is now subscribed to topic: {command_topic}")
				
		except Exception as e:
			logging.error("EXCEPTION RAISED ON_CONNECT: " + str(e))

		logging.info("Connected to the MQTT Broker successfully")
        

	def on_message(self, client, userdata, message):
		"""
		Callback for receiving messages from the MQTT broker.

		:param client: The client instance for this callback.
		:param userdata: The private user data as set in Client() or userdata_set.
		:param message: The message received from the broker.
		"""
		logging.info(f"{message.topic} MSG: {message.payload.decode()} with QoS {message.qos}")

		try:
			self.handle_action(message.topic, message.payload.decode())
			
		except Exception as e:
			logging.error(f"EXCEPTION RAISED ON_MESSAGE: {e}")
	
			
	def handle_action(self, topic:str, payload:str):
		
		json_data = json.loads(payload)
		action = json_data.get('action')
		args = json_data.get('args', {})
		args['client'] = self.MideaClient
		
		# the action should be one available on one of the devices
		for appliance in self.appliances:
			
			if hasattr(appliance, action):
				method = getattr(appliance, action)
				logging.info (f"Action {method} will be done on device {appliance.id}")
				ret = method(**args)
						
			else:
				logging.warning(f"No method named {action} found in {appliance.id}")

		
		
