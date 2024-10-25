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

import yeelight
from .YeelightLamp import YeelightLamp
from .YeelightConfig import YeelightConfig


from .const import (
	NAME,
	VERSION,
)

__version__ = VERSION


class YeelightPool():
	"""A class to manage a pool of Yeelight smart bulbs and their MQTT integration.
    The integration comes in the form of /<level0>/<level1>/attribute"""

	def __init__(self, brokerIP:str = '127.0.0.1', brokerPort:int = 1883, 
				log_to_file: bool = False, log_file: str = "YeelightPool.log",
				debug: bool = False):
		"""Initialize the YeelightPool.

		Args:
		    brokerIP (str): IP address of the MQTT broker.
		    brokerPort (int): Port of the MQTT broker.
		    log_to_file (bool): Whether to log to a file.
		    log_file (str): Name of the log file.
		    debug (bool): Whether to enable debug-level logging.
		"""
		self.debug = debug
		self.log_to_file = log_to_file
		self.log_file = log_file
		self.stop_event = threading.Event()
        
		self.lamps = []

		self.brokerIP = brokerIP
		self.brokerPort = brokerPort
		
		self._setup_logging()
		

	def _setup_logging(self):
		"""Sets up the logging configuration for the class."""
		if self.log_to_file:
			logging.basicConfig(filename=self.log_file, level=logging.DEBUG if self.debug else logging.INFO)
		else:
			logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if self.debug else logging.INFO)
			
            
	def start(self, yeelight_lamps:list, yeelight_level0:list, yeelight_level1:list):
		"""Start the YeelightPool by creating and starting lamps.

		Args:
		    yeelight_lamps (list): List of Yeelight lamp IPs.
		    yeelight_level0 (list): List of room topics.
		    yeelight_level1 (list): List of device topics.

		Raises:
		    AssertionError: If the length of the lists don't match.
		"""		
		assert len(yeelight_lamps) == len(yeelight_level0), (f"Number of topics ({len(yeelight_lamps)}) differs from number of rooms ({len(yeelight_level0)})")
		assert len(yeelight_lamps) == len(yeelight_level1), (f"Number of topics ({len(yeelight_lamps)}) differs from number of devices ({len(yeelight_level1)})")

		logging.info(f"Creating Lamps . . .")
		self._add_lamps(yeelight_lamps, yeelight_level0, yeelight_level1)
		logging.info(f"Number of lamps added {len(yeelight_lamps)}")
		self._start_lamps()
	
		try:		
			while not self.stop_event.is_set():
				time.sleep(1)
		except KeyboardInterrupt:
			self.stop()

		# Wait for threads to finish
		for lamp in self.lamps:
			logging.info(f"Waiting to terminate {lamp['thread']}")
			lamp['thread'].join()
		
		logging.info(f"Terminated YeelightPool")
		

	def stop(self):
		"""Stop the YeelightPool and gracefully shut down all threads."""
		logging.info("Stopping YeelightPool System...")
		self.stop_event.set()

		
	def _start_lamps(self):
		"""Start all the lamps in separate threads."""		
		for lamp in self.lamps:
			lamp['thread'].start()
			
		
	def _add_lamps(self, yeelight_lamps:list, yeelight_level0:list, yeelight_level1:list):
		"""Add lamps to the pool and create their corresponding threads.

		Args:
		    yeelight_lamps (list): List of Yeelight lamp IPs.
		    yeelight_level0 (list): List of room topics.
		    yeelight_level1 (list): List of device topics.
		"""		
		for lamp_ips in yeelight_lamps:
			try:
				index = yeelight_lamps.index(lamp_ips)
				level0 = yeelight_level0[index]
				level1 = yeelight_level1[index]
			except ValueError: # value not found in the config file
				raise ValueError(f"Key not found: {lamp_ips}")					
				
			print(f"Creating lamps {lamp_ips}")
			new_lamp = YeelightLamp(lamp_ips, level0, level1, self.brokerIP, self.brokerPort, self.stop_event)
			self.lamps.append({
				"lamp": new_lamp,
				"thread": threading.Thread(target=new_lamp.start, name=f"/{level0}/{level1}")
				})


