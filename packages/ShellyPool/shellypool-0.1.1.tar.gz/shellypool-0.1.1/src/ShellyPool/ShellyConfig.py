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
from configparser import ConfigParser

class ShellyConfig():

	def __init__(self, filename='config.cfg'):
		self.parser = ConfigParser()
		self.filename = filename
		self.parser.read(filename)
		

	def read(self, section='section'):

		cfg = {}
		if self.parser.has_section(section):
			params = self.parser.items(section)
			for param in params:
				cfg[param[0]] = param[1]
		else:
			raise Exception('Section {0} not found in the {1} file'.format(section, filename))

		return cfg
