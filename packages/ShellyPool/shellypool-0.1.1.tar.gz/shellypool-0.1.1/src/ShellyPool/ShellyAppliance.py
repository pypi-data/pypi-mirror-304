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
from pyShelly import Device
import paho.mqtt.client as mqtt
import time
import json
import threading

class ShellyAppliance():

	def __init__(self, id_appliance:str, room:str='room', name:str='appliance', brokerIP:str = '127.0.0.1', brokerPort:int = 1883, stop_event=threading.Event):
		self.id = id_appliance
		self.mqtt_topic = self.id
		self.room = room
		self.name = name
		self.devices = [] # these are the shelly devices obtained after the discovery per IP
		self.attributes = {}
		self.stop_event = stop_event
		
		self.brokerIP = brokerIP
		self.brokerPort = brokerPort
		self.clientBroker = mqtt.Client()
		
		# start listening to MQTT messages in another thread
		self.start_thread = threading.Thread(target=self.start, name=id_appliance)
		self.start_thread.start()
		

	@property
	def ip_addr(self):
		assert len(self.devices) > 0, (f"No devices connected to this appliance")
		return self.devices[0].ip_addr	# all devices will be encapsulated within the same IP

		
	def add_device(self, device:Device):
		self.devices.append(device)
		
	def _get_new_topic(self, attribute:str, payload:str):
		return f"/{self.room}/{self.name}/{attribute}", payload
		

	def start(self):
		
		# Start MQTT loop in the background
		self.clientBroker.on_connect = self.on_connect
		self.clientBroker.on_message = self.on_message
		self.clientBroker.connect(self.brokerIP, self.brokerPort)
		self.clientBroker.loop_start()

		while not self.stop_event.is_set():
			time.sleep(1)

        # Wait for threads to finish
		self.clientBroker.disconnect()
		
		
	def on_connect(self, client, userdata, flags, rc):
		"""
		Callback for successful connection to the MQTT broker.

		:param client: The client instance for this callback.
		:param userdata: The private user data as set in Client() or userdata_set.
		:param flags: Response flags sent by the broker.
		:param rc: Connection result code.
		"""

		try:
			command_topic = f"/{self.room}/{self.name}/command"
			client.subscribe(command_topic, 0)	# subscribe to all commands to this device
			print(f"{self.id} is now subscribed to topic: {command_topic}")
				
		except Exception as e:
			print("EXCEPTION RAISED ON_CONNECT: " + str(e))

		print("Connected to the MQTT Broker successfully")
        

	def on_message(self, client, userdata, message):
		"""
		Callback for receiving messages from the MQTT broker.

		:param client: The client instance for this callback.
		:param userdata: The private user data as set in Client() or userdata_set.
		:param message: The message received from the broker.
		"""
		print(f"{message.topic} MSG: {message.payload.decode()} with QoS {message.qos}")

		try:
			self.handle_action(message.topic, message.payload.decode())
			
		except Exception as e:
			print(f"EXCEPTION RAISED ON_MESSAGE: {e}")
	
			
	def handle_action(self, topic:str, payload:str):
		
		json_data = json.loads(payload)
		action = json_data.get('action')
		args = json_data.get('args', {})
		
		# the action should be one available on one of the devices
		for dev in self.devices:
			
			if hasattr(dev, action):
				print(f"Action will be done on device {dev.device_type}")
				method = getattr(dev, action)
				method(**args)
							
			#else:
			#	print(f"No method named {action} found in {dev.device_name} - {dev.device_type}	")
			
	def _get_new_topic(self, attribute:str, payload:str):
		return f"/{self.room}/{self.name}/{attribute}", payload
