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

from pyShelly import pyShelly, SHELLY_TYPES
from .ShellyAppliance import ShellyAppliance
from .ShellyHTSensor import ShellyHTSensor
from .ShellyPlugS import ShellyPlugS
from .ShellyButton import ShellyButton
from .ShellyConfig import ShellyConfig


from .const import (
	NAME,
	VERSION,
	TIMEOUT_DISCOVERY,
	SHELLY_TYPE_CLASS
)

__version__ = VERSION


class ShellyPool():

	def __init__(self, brokerIP:str = '127.0.0.1', brokerPort:int = 1883, 
				log_to_file: bool = False, log_file: str = "ShellyPool.log",
				debug: bool = False):

		self.debug = debug
		self.log_to_file = log_to_file
		self.log_file = log_file
		self.stop_event = threading.Event()
		
		self.shelly_topics = None
		shelf_shelly_level0 = None
		shely_shelly_level1 = None
        
		self.pool = {}
		self.shelly = pyShelly()

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
			
            
	def start(self, shelly_topics:list, shelly_level0:list, shelly_level1:list):
		
        # Validate the lengths of input lists
		assert len(shelly_topics) == len(shelly_level0), (f"Number of topics ({len(shelly_topics)}) differs from number of level0 items ({len(shelly_level0)})")
		assert len(shelly_topics) == len(shelly_level1), (f"Number of topics ({len(shelly_topics)}) differs from number of level1 items ({len(shelly_level1)})")

		logging.info(f"Discovering devices . . .")
		self.shelly_topics = shelly_topics
		self.shelly_level0 = shelly_level0
		self.shelly_level1 = shelly_level1
		self._discover()
		logging.info(f"Number of devices discovered {len(self.pool)}")


        # Start MQTT loop in the background
		logging.info(f"Listening now to topics")
		self.clientBroker.on_connect = self.on_connect
		self.clientBroker.on_message = self.on_message
		self.clientBroker.connect(self.brokerIP, self.brokerPort)
		self.clientBroker.loop_start()
		
		try:
		# Main loop to keep the system running until a stop signal is received
		
			while not self.stop_event.is_set():
				time.sleep(1)
				
		except KeyboardInterrupt:
			self.stop()

		# Wait for threads to finish
		for key, device in self.pool.items():
			logging.info(f"Waiting to terminate {device.id}")
			device.start_thread.join()
		
		self.clientBroker.disconnect()
		self.shelly.close()
		logging.info(f"Terminated ShellyPool")
		

	def stop(self):
		"""Triggers the stop event to gracefully shutdown all threads."""
		logging.info("Stopping ShellyPool System...")
		self.stop_event.set()
				
		
	def _discover(self):

		self.shelly.cb_device_added.append(self._on_device_connected)
		
		self.shelly.start()
		

	def _on_device_connected(self, device, code):
		
			try:
				mqtt_topic = f"shellies/{SHELLY_TYPES[device.type]['mqtt']}-{device.id}"
				index = self.shelly_topics.index(mqtt_topic)
				level0 = self.shelly_level0[index]
				level1 = self.shelly_level1[index]
			except ValueError: # value not found in the config file
				raise (f"Key not found: {mqtt_topic}")					
			
			# create object
			if mqtt_topic not in self.pool.keys():
				self.pool[mqtt_topic] = SHELLY_TYPE_CLASS.get(device.type, ShellyAppliance)(mqtt_topic, level0, level1, self.brokerIP, self.brokerPort, self.stop_event)
					
			self.pool[mqtt_topic].add_device(device)			
			
			# Subscription to mqtt_topic
			try:
				self.clientBroker.subscribe(f"{mqtt_topic}/#", 0)
				logging.info(f"Subscribed to topic: {mqtt_topic}")
			except Exception as e:
				logging.error("EXCEPTION RAISED ON_CONNECT: " + str(e))

			
	def on_connect(self, client, userdata, flags, rc):
		"""
		Callback for successful connection to the MQTT broker.

		:param client: The client instance for this callback.
		:param userdata: The private user data as set in Client() or userdata_set.
		:param flags: Response flags sent by the broker.
		:param rc: Connection result code.
		"""
		logging.info(f"Connected with result code {rc}")

		try:
			# Subscribe to topics upon connection
			for key, device in self.pool.items():
				client.subscribe(f"{key}/#", 0)
				logging.info(f"Subscribed to topic: {key}")
				
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
			
			for topic, obj in self.pool.items():
				if message.topic.startswith(topic):
					payload = message.payload.decode()
					attribute = message.topic[len(topic) + 1:]

					# Determine the new topic based on the attribute
					new_topic, value = obj._get_new_topic(attribute, payload)

					client.publish(new_topic, value)
					logging.info(f"Published topic: {new_topic}: {value}")

		except Exception as e:
			logging.info(f"EXCEPTION RAISED ON_MESSAGE: {e}")


