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
from yeelight import Bulb, BulbException
from .YeelightBulb import YeelightBulb

import paho.mqtt.client as mqtt
import threading
import time
import json

class YeelightLamp():
	"""A class for grouping bulbs into lamps."""
    
	def __init__(self, bulbs_ips:list, level0:str='room', level1:str='appliance', brokerIP:str = '127.0.0.1', brokerPort:int = 1883, stop_event=threading.Event()):
		"""Initialize the YeelightLamp.
		
		Args:
			bulbs_ips (list): IP address of the bulbs conforming this lamp.
			level0 (str): level0 of the MQTT Topic it serves to (/<level0>/<level1>/attribute).
			level1 (str): level1 of the MQTT Topic it serves to (/<level0>/<level1>/attribute).
			brokerIP (str): IP address of the MQTT broker.
			brokerPort (int): Port of the MQTT broker.
			stop_event (threading.Event): flag to stop processes.

		"""
		self.level0 = level0
		self.level1 = level1
		self.mqtt_topic = f"/{level0}/{level1}"
		self.devices = [] # these are the yeelight devices obtained after the discovery per IP
		self.stop_event = stop_event

		self.brokerIP = brokerIP
		self.brokerPort = brokerPort
		self.clientBroker = mqtt.Client()

		# Start listening to each bulb for changes
		for ip in bulbs_ips:
			try:
				bulb = YeelightBulb(ip)
				self.devices.append({
					"bulb": bulb,
					"thread": threading.Thread(target=self.listen_to_bulb, args=(bulb,), daemon=True, name=ip)
					})
				bulb.set_rgb(128, 128, 128)
				bulb.set_brightness(80)
			except BulbException as be:
				print(f"EXCEPTION Operating with bulb: {be}")
			except Exception as e:
				print(f"EXCEPTION: {e}")
				
		

	@property
	def properties(self):
		"""Retrieve the values of the lamp. The attributes for individual bulbs may be
		different to each other. In that case, either a new value is provided (e.g. partial)
		or a range is given (eg. 125-255)

		Returns:
			dict: properties of the lamp.

		"""
		try:
			threshold = 0.1
			lamp_properties = self.devices[0]['bulb'].properties
			
			# Power properties
			power_states = [ bulb['bulb'].properties['power'] for bulb in self.devices ]
			if all(state == 'on' for state in power_states):
				lamp_properties['power'] = 'on'
			elif all(state == 'off' for state in power_states):
				lamp_properties['power'] = 'off'
			else:
				lamp_properties['power'] = 'partial'
				
				
			# for numerical values, the difference in values can be considered (by agreement)
			# the same if they do not differ more than 10% from the others.
			# color_temp property, between 1700-6500
			ct_states = [ int(bulb['bulb'].properties['ct']) for bulb in self.devices ]
			if ( max(ct_states) - min(ct_states) ) / (6500-1700) > threshold:
				lamp_properties['ct'] = f"{min(ct_states)}-{max(ct_states)}"
			
			# rgb property, between 0-16777215
			rgb_states = [ int(bulb['bulb'].properties['rgb']) for bulb in self.devices ]
			if ( max(ct_states) - min(ct_states) ) / 16777215 > threshold:
				lamp_properties['rgb'] = f"{min(rgb_states)}-{max(rgb_states)}"

			# hue property, between 0-359
			hue_states = [ int(bulb['bulb'].properties['hue']) for bulb in self.devices ]
			if ( max(hue_states) - min(hue_states) ) / 100 > threshold:
				lamp_properties['hue'] = f"{min(hue_states)}-{max(hue_states)}"
			
			# sat property, between 0-100
			sat_states = [ int(bulb['bulb'].properties['sat']) for bulb in self.devices ]
			if ( max(sat_states) - min(sat_states) ) / 100 > threshold:
				lamp_properties['sat'] = f"{min(sat_states)}-{max(sat_states)}"
				
			# brightness property, between 1-100
			brightness_states = [ int(bulb['bulb'].properties['bright']) for bulb in self.devices ]
			if ( max(brightness_states) - min(brightness_states) ) / 100 > threshold:
				lamp_properties['bright'] = f"{min(brightness_states)}-{max(brightness_states)}"

		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")
		
		return lamp_properties
		

	def set_brightness(self, brightness:int):
		"""Set the brightness of the lamp

		Args:
			brightness (int): brightness value.
		"""

		try:
			for device in self.devices:
				device['bulb'].set_brightness(brightness)
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")		
			
	
	def set_color_temp(self, degrees:int):
		"""Set the color temperature of the lamp

		Args:
			degrees (int): color temp value.
		"""		
		try:
			for device in self.devices:
				device['bulb'].set_color_temp(degrees)
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")
			
	
	def set_hsv(self, hue:int, sat:int, value:int):
		"""Set the hsv of the lamp

		Args:
			hue (int): hue value.
			sat (int): saturation value.
			value (int): value
		"""		
		try:
			for device in self.devices:
				device['bulb'].set_hsv(hue, sat, value)
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")
			
	
	def set_power_mode(self, mode:int):
		"""Set the power mode of the lamp

		Args:
			mode (int): mode value.
		"""		
		try:
			for device in self.devices:
				device['bulb'].set_power_mode(mode)
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")

			
	
	def set_rgb(self, red:int, green:int, blue:int):
		"""Set the RGB of the lamp

		Args:
			red (int): red value.
			green (int): green value.
			blue (int): blue value.
		"""		
		try:
			for device in self.devices:
				device['bulb'].set_rgb(red, green, blue)
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")
			
	
	def toggle(self):
		"""Toggle power of the lamp"""
		try:
			for device in self.devices:
				device['bulb'].toggle()
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")
			
	
	def turn_off(self):
		"""Turn off the lamp"""
		try:
			for device in self.devices:
				device['bulb'].turn_off()
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")
			
	
	def turn_on(self):
		"""Turn on the lamp"""
		try:
			for device in self.devices:
				device['bulb'].turn_on()			
		except BulbException as be:
			print(f"EXCEPTION Operating with bulb: {be}")
		except Exception as e:
			print(f"EXCEPTION: {e}")
	

	def on_bulb_state_change(self, bulb, event):
		"""
		Callback function to replicate the changes in all other bulbs when one changes.
		"""
		print(f"Change detected in bulb {bulb._ip}: {event}")

		# Publish on the MQTT
		for key, value in self.properties.items():
			self.clientBroker.publish(f"/{self.level0}/{self.level1}/{key}", value)


	def listen_to_bulb(self, bulb):
		"""
		Start listening for changes in a given bulb and trigger state replication.
		"""
		bulb.listen(lambda event: self.on_bulb_state_change(bulb, event))
        

	def start(self):
		"""Start the YeelightLamp processes and connection to the MQTT."""		
		# Start MQTT loop in the background
		self.clientBroker.on_connect = self.on_connect
		self.clientBroker.on_message = self.on_message
		self.clientBroker.connect(self.brokerIP, self.brokerPort)
		self.clientBroker.loop_start()
		
		for device in self.devices:
			device['thread'].start()

		while not self.stop_event.is_set():			
			time.sleep(1)

        # Wait for threads to finish and close connection to MQTT Broker
        # although threads are running as daemons
		for device in self.devices:
			#device['thread'].join()
			pass

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
			command_topic = f"{self.mqtt_topic}/command"
			client.subscribe(command_topic, 0)	# subscribe to all commands to this device
			print(f"{self.level1} is now subscribed to topic: {command_topic}")
				
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
		"""Handle the command to execute.
				
		Args:
			topic (str): topic to refering to command (/<level0>/<level1>/command).
			payload (str): payload including action and args to execute as JSON
		"""
		# ensure the payload is json and avoid single quote \'
		json_data = json.loads(payload)
		action = json_data.get('action')
		args = dict(json_data.get('args', {}))
		
		# the action should be one available on one of the devices
		for dev in self.devices:			
			if hasattr(dev['bulb'], action):
				print(f"Action will be done on device {dev['bulb']}")
				method = getattr(dev['bulb'], action)
				if args:
					method(**args)
				else:
					method()
											
			#else:
			#	print(f"No method named {action} found in {dev.device_name} - {dev.device_type}	")


