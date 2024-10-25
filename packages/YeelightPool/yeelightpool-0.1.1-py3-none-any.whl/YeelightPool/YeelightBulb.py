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

class YeelightBulb(Bulb):
    """A class extending the Yeelight Bulb class for additional functionalities."""
    
    def __init__(self, ip:str, port:int=55443, effect:str='smooth', duration:int=300, auto_on:bool=False, power_mode=None, model=None):
        """Initialize the YeelightBulb

        Args:
            ip (str): IP address of the bulb.
            port (int): Port of the bulb.
            effect (str): The effect to use during transitions.
            duration (int): Duration of transitions in milliseconds.
            auto_on (bool): Whether to automatically turn on the bulb if it's off.
            power_mode: Power mode to use when turning on the bulb.
            model: Specific model of the Yeelight bulb.
	"""
        super().__init__(ip, port, effect, duration, auto_on, power_mode, model)
    
    
    @property
    def properties(self):
        """Retrieve properties of the Yeelight bulb."""
        return self.get_properties()
