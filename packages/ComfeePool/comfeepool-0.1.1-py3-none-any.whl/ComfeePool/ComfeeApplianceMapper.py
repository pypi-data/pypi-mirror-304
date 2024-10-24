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

import sys
import getopt
import time
import datetime
import logging

class ComfeeApplianceMapper():
	
	def __init__(self, id_appliance:str, level0:str='level0', level1:str='level1'):
		self.id = id_appliance
		self.level0 = level0
		self.level1 = level1
		self.attributes = {}


	def mqttTopics_to_update(self, appliance):
		return {}		
		
			
	def _get_new_topic(self, attribute:str, payload:str):
		return f"/{self.level0}/{self.level1}/{attribute}", payload
