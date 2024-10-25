# YeelightPool
A package to integrate Yeelight Bulbs with MQTT Brokers. This package intends to integrate Bulbs into Lamps within the network and manage it as a pool of devices that can be accessible through the MQTT Broker.

## Introduction
The package is intended to establish an MQTT interface with the Yeelight device. The equipment attributes will be readable in the MQTT Broker through a topic in the form _/\<level0>/\<level1>/attribute_. The equipment will be located within a hierarchy of levels in the MQTT Broker, being the device located into 2 levels, typically _location_ and _equipment_, and within the equipment all the attributes of this device.

The special attribute _/\<level0>/\<level1>/\<command>_ is serving as a special attribute to send commands to the device. The commands are those available from the library _yeelight_ and the function behind this package simply wraps a json command with its arguments. This json content is simply passed onto the package ___yeelight___ and executes the command onto the equipment. The json document including the execution of a command is in the form:
<pre>
{
	"action": "name of the method",
	"args": "{
				"arg1": "value 1",
				"arg2": "value 2",
				"argN": "value N"
			}
}
</pre>

The name of the the method is one of the ___yeelight___ methods. 

## Workflow diagram
The device and the MQTT have the following communication diagram
```mermaid
sequenceDiagram
Device ->> YeelightPool: Device Status
YeelightPool -->> MQTT Broker: Publish Topics
MQTT Broker ->> User Program: Status attributes 
User Program ->> MQTT Broker: { command, args }
MQTT Broker -->> YeelightPool: Subscribe Topics<br/>(command)
YeelightPool ->> Device: Function call<br/> Execution command
Note right of User Program: Async calls to execute<br/>commands on device.
```
## Configuration file
The package gives the possibility to configure parameters through a configuration file. This file can be, as an example, like this:
>[yeelight]
>logfile=yeelightpool.log
>lamps=[ ["192.168.0.101", "192.168.0.102"], ["192.168.0.103"] ]
>room=[ "Living Room", "Kids Room" ]
>device=[ "Ceiling Lamp", "Desk Lamp" ]
>
>[broker]
>ip=127.0.0.1
>port=1883

The configuration file will be splitted into two areas:
- [yeelight]: this area defines the lamps as a serie of bulb's ip addresses. The room name for the lamps. And the device name of the lamp. It also gives the chance to log data to a logfile.
- [broker]: this is the broker ip:port to connect to. This broker is to be setup apart from this package.


## How to install
To install the library just execute:
> pip install YeelightPool

## Example
> import sys
import YeelightPool
>
>def main():
>     # Configuration of the Shelly device
>     config = YeelightPool.YeelightConfig(sys.argv[1])
>     params_yeelight = config.read(section="yeelight")
>     params_broker = config.read(section="broker")
>
> print(f"Yeelight Devices Pool Version {YeelightPool.__version__}")
    print(f"Creating Pool of Yeelight Devices . . . ", end="")
    pool = YeelightPool.YeelightPool(params_broker['ip'], int(params_broker['port']))
    print(f"[ OK ]")
>
>    print(f"Running the pool")
    pool.start(
        eval(params_yeelight['lamps']), 
        eval(params_yeelight['room']), 
        eval(params_yeelight['device'])
        )
   > 
   > print(f"Finalizing Yeelight Pool . . . [ OK ]")
    >
>if __name__ == "__main__":
> main()

## Release Notes
**0.1.1** - Initial release

# Credits
 - yeelight - https://pypi.org/project/yeelight/
