from midea_inventor_lib import MideaClient
import threading

from .ComfeeApplianceMapper import ComfeeApplianceMapper


class ComfeeDehumidifierMapper(ComfeeApplianceMapper):

	def __init__(self, id_appliance:str, level0:str='level0', level1:str='level1'):
		
		self._powerMode = None
		self._setMode = None
		self._humidity = None
		self._humidity_set = None
		self._humidity_dot = None
		self._humidity_dot_set = None
		self._windSpeed = None
		self._ionSetSwitch = None
		self._isDisplay = None
		self._filterShow = None
		self._tankShow = None
		self._dryClothesSetSwitch = None
		self._upAndDownSwing = None		

		super().__init__(id_appliance, level0, level1)


	#
	# Here it is the specifics for the device, redefiniting the functions.
	#	
	def mqttTopics_to_update(self, appliance):
		topics = []
				
		if self.powerMode != appliance.powerMode:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/power",
						'value': 'on' if appliance.powerMode==1 else 'off'
						})
			self._powerMode = appliance.powerMode
			
		if self.setMode != appliance.setMode:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/setMode",
						'value': appliance.setMode
						})
			self._setMode = appliance.setMode
		
		if self.humidity != appliance.humidity:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/humidity",
						'value': appliance.humidity
						})
			self._humidity = appliance.humidity

		if self.humidity_set != appliance.humidity_set:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/humidity_target",
						'value': appliance.humidity_set
						})
			self.humidity_set = appliance.humidity_set
			
		if self.humidity_dot != appliance.humidity_dot:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/humidity_dot",
						'value': appliance.humidity_dot
						})
			self.humidity_dot = appliance.humidity_dot

		if self.humidity_dot_set != appliance.humidity_dot_set:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/humidity_dot_target",
						'value': appliance.humidity_dot_set
						})
			self.humidity_dot_set = appliance.humidity_dot_set
		
		if self.windSpeed != appliance.windSpeed:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/windSpeed",
						'value': appliance.windSpeed
						})
			self.windSpeed = appliance.windSpeed

		if self.ionSetSwitch != appliance.ionSetSwitch:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/ionSetSwitch",
						'value': appliance.ionSetSwitch
						})
			self.ionSetSwitch = appliance.ionSetSwitch

		if self.isDisplay != appliance.isDisplay:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/isDisplay",
						'value': appliance.isDisplay
						})
			self.isDisplay = appliance.isDisplay

		if self.filterShow != appliance.filterShow:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/filterShow",
						'value': appliance.filterShow
						})
			self.filterShow = appliance.filterShow

		if self.tankShow != appliance.tankShow:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/tankShow",
						'value': appliance.tankShow
						})
			self.tankShow = appliance.tankShow

		if self.dryClothesSetSwitch != appliance.dryClothesSetSwitch:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/dryClothesSetSwitch",
						'value': appliance.dryClothesSetSwitch
						})
			self.dryClothesSetSwitch = appliance.dryClothesSetSwitch

		if self.upAndDownSwing != appliance.upAndDownSwing:
			topics.append({
						'topic': f"/{self.level0}/{self.level1}/upAndDownSwing",
						'value': appliance.upAndDownSwing
						})
			self.upAndDownSwing = appliance.upAndDownSwing
			
		return topics

	
	@property
	def powerMode(self):
		return self._powerMode
		
	@powerMode.setter
	def powerMode(self, value):
		self._powerMode = value

	@property
	def setMode(self):
		return self._setMode
		
	@setMode.setter
	def setMode(self, value):
		self._setMode = value

	@property
	def humidity(self):
		"""Return the current humidity"""
		return self._humidity

	@humidity.setter
	def humidity(self, value):
		self._humidity = value
		
	@property
	def humidity_set(self):
		"""Return the target humidity"""
		return self._humidity_set

	@humidity_set.setter
	def humidity_set(self, value):
		self._humidity_set = value
		
	@property
	def humidity_dot(self):
		"""Return the current humidity (decimal)"""
		return self._humidity_dot

	@humidity_dot.setter
	def humidity_dot(self, value):
		self._humidity_dot = value
		
	@property
	def humidity_dot_set(self):
		"""Return the target humidity (decimal)"""
		return self._humidity_dot_set

	@humidity_dot_set.setter
	def humidity_dot_set(self, value):
		self._humidity_dot_set = value
		
	@property
	def windSpeed(self):
		return self._windSpeed
		
	@windSpeed.setter
	def windSpeed(self, value):
		self._windSpeed = value

	@property
	def ionSetSwitch(self):
		return self._ionSetSwitch

	@ionSetSwitch.setter
	def ionSetSwitch(self, value):
		self._ionSetSwitch = value
		
	@property
	def isDisplay(self):
		return self._isDisplay

	@isDisplay.setter
	def isDisplay(self, value):
		self._isDisplay = value
		
	@property
	def filterShow(self):
		return self._filterShow

	@filterShow.setter
	def filterShow(self, value):
		self._filterShow = value
		
	@property
	def tankShow(self):
		return self._tankShow

	@tankShow.setter
	def tankShow(self, value):
		self._tankShow = value
		
	@property
	def dryClothesSetSwitch(self):
		return self._dryClothesSetSwitch

	@dryClothesSetSwitch.setter
	def dryClothesSetSwitch(self, value):
		self._dryClothesSwitch = value
		
	@property
	def upAndDownSwing(self):
		return self._upAndDownSwing
			
	@upAndDownSwing.setter
	def upAndDownSwing(self, value):
		self._upAndDownSwing = value


	def turn_on(self, client:MideaClient=None):
		if client is not None:
			return client.send_poweron_command(self.id)
			
			
	def turn_off(self, client:MideaClient=None):
		if client is not None:
			return client.send_poweroff_command(self.id)
		
		
	def ion_on(self, client:MideaClient=None):
		if client is not None:
			return client.send_ion_on_command(self.id)

		
	def ion_off(self, client:MideaClient=None):
		if client is not None:
			return client.send_ion_off_command(self.id)
			
		
	def fan_speed(self, client:MideaClient=None, speed:int=60):
		if client is not None:
			return client.send_fan_speed_command(self.id, speed)
			
			
	def fan_speed_silent(self, client:MideaClient=None):
		if client is not None:
			return client.send_fan_speed_silent_command(self.id)
		
		
	def fan_speed_medium(self, client:MideaClient=None):
		if client is not None:
			return client.send_fan_speed_medium_command(self.id)
			
			
	def fan_speed_high(self, client:MideaClient=None):
		if client is not None:
			return client.send_fan_speed_high_command(self.id)
			
			
	def target_humidity(self, client:MideaClient=None, humidity:int=40):
		if client is not None:
			return client.send_target_humidity_command(self.id, humidity)
			
			
	def target_mode(self, client:MideaClient=None):
		if client is not None:
			return client.send_target_mode_command(self.id)
			
			
	def continous_mode(self, client:MideaClient=None):
		if client is not None:
			return client.send_continous_mode_command(self.id)
			
			
	def smart_mode(self, client:MideaClient=None):
		if client is not None:
			return client.send_smart_mode_command(self.id)
			
			
	def dryer_mode(self, client:MideaClient=None):
		if client is not None:
			return client.send_dryer_mode_command(self.id)
			
			
	
			
