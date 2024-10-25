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
from ShellyPool import ShellyAppliance
import threading


class ShellyButton(ShellyAppliance):

	def __init__(self, id_appliance:str, room:str='room', name:str='appliance', brokerIP:str = '127.0.0.1', brokerPort:int = 1883, stop_event=threading.Event):

		super().__init__(id_appliance, room, name, brokerIP, brokerPort, stop_event)


	#
	# Here it is the specifics for the device, redefiniting the functions.
	#
	
	def _get_new_topic(self, attribute:str, payload:str):
		
		pl = payload
		
		if attribute == 'sensor/battery':
			att = "battery"
			
		elif attribute == 'sensor/charger':
			pl = True if payload == 'true' else False
			att = "charger"

		elif attribute == 'sensor/error':
			pl = True if payload == '1' else False
			att = "error"

		elif attribute == 'sensor/act_reasons':
			att = "act_reasons"
			
		elif attribute =='input_event/0':
			att = 'event'

		else:
			att = attribute

		self.attributes[att] = pl
		return f"/{self.room}/{self.name}/{att}", pl

			

