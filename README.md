[![Build](https://github.com/Chibald/MaestroGateway/workflows/Build/badge.svg)](https://github.com/Chibald/maestrogateway/actions?query=workflow%3ABuild)
[![Standalone](https://github.com/Chibald/MaestroGateway/workflows/Standalone/badge.svg)](https://github.com/Chibald/maestrogateway/actions?query=workflow%3AStandalone)
[![Daemon Service](https://github.com/Chibald/MaestroGateway/workflows/Daemon%20Service/badge.svg)](https://github.com/Chibald/maestrogateway/actions?query=workflow%3A%22Daemon+Service%22)

![Warning](https://github.com/Chibald/maestrogateway/blob/master/docs/disclaimer.png?raw=true)

This is a script for relaying messages to a MCZ Maestro pellet stove. All of this software is provided AS-IS with no implied warranty or liability under sections 15, and 16 of the GPL V3. So if your stove burns down your house, it's not my fault.

# MCZ Maestro Equipment Gateway with Mqtt / JSON
Python script for controlling Pellet Stoves using Maestro technology.

It is known to work with newer pellet stoves from MZC
Personally I use it using a MCZ Musa Hydro stove.

## About Maestro
Maestro technology uses a Websocket to communicatie with the pellet stove. It is used by the MZC Maestro App and also by external thermostats.
https://www.mcz.it/en/maestro-technology/

## Usage
This script returns the websocket data and will publish it on MQTT topics which you can use in your home automation software. You can use this information to display the state of all parameters from the stove. Also all basic commands that you can send using the official MZC app are available on another MQTT topic.

It can be installed locally or using docker, get the latest build from https://hub.docker.com/r/chibald/maestrogateway

### Configuration
Configure by setting varables in _config_.py when running in local python mode, or by setting environment variables in docker.

| Variable | Description |
| ----------------------- | ----------- |
| `MQTT_ip`| Mqtt broker address
| `MQTT_port`| Mqtt broker port, default 1883
| `MQTT_authentication`| use authentication, True / False
| `MQTT_user`| Mqtt User name
| `MQTT_pass`| Mqtt password
| `MQTT_TOPIC_SUB`| Mqtt topic for command messages here
| `MQTT_TOPIC_PUB`| Information messages by daemon are published here
| `MQTT_PAYLOAD_TYPE`| Payload as seperate subtopic (_MQTT_PAYLOAD_TYPE='TOPIC') or as JSON (_MQTT_PAYLOAD_TYPE='JSON')
| `WS_RECONNECTS_BEFORE_ALERT`| Attempts to reconnect to webserver before publishing a alert on topic PUBmcz/Status
| `MCZip`| Stove IP Address. Default is 192.168.120.1
| `MCZport`| Stove websocket port. Default is 81


### Recieving information
Data is polled from the stove every 15 seconds.

#### Payload type Json
If you use the Json payload type all the parameters wille be published to one topic using a json object:

```
{ "Stove_State": 0, "Fan_State": 1, "DuctedFan1": 0.0, "DuctedFan2": 0.0, "Fume_Temperature": 22.5, "Ambient_Temperature": 19.5, "Puffer_Temperature": 127.5, "Boiler_Temperature": 51.0, "NTC3_Temperature": 127.5, "Candle_Condition": 0, "ACTIVE_Set": 150, "RPM_Fam_Fume": 0, "RPM_WormWheel_Set": 0, "RPM_WormWheel_Live": 0, "3WayValve": "Risc", "Pump_PWM": 0, "Brazier": "OK", "Profile": 1, "Modbus_Address": 41, "Active_Mode": 1, "Active_Live": 99, "Control_Mode": 1, "ECO_Mode": 1, "Silent_Mode": 0, "Chrono_Mode": 1 
.....
```
the script will check if value has changed, so next messages are filtered for changes vakues only

for example:
```
{"Ambient_Temperature": 19.0}
```
#### Payload type topic
If you use payload type Topic, all the parameters will be published to a separate topic under the `MQTT_TOPIC_PUB` topic for example
```
Maestro/Status/Ambient_Temperature, 19.0
```

### Sending commands
Publish Json command on the command Mqtt - topic to issue commands.

#### Payload type Json
Examples:
to turn on the stove:
```
{ "Command": "Power", "Value": 1}
```

to turn off the stove:
```
{ "Command": "Power", "Value": 0}
```

to set temperature to 20.5 degrees:
```
{ "Command": "Temperature_Setpoint", "Value": "20.5"}
```

#### payload type Topic
to turn on the stove:
```
Maestro/Set/Power, 1
```

to turn off the stove:
```
Maestro/Set/Power, 0
```

to set temperature to 20.5 degrees:
```
Maestro/Set/Power/Temperature_Setpoint, 20.5
```

## Hardware Prerequisities
The MCZ pellet stove has its own Wifi SSID. The easiest way to bridge this connection is by using a Raspberry pi with a wired ethernet to your lan, and to configure the onboard Wifi to connect to the SSID of the pellet stove. But any with two interface and at least one wifi interface to connect to the stove will work.

## Software Prerequisities
You will need a Home Automation software with MQTT broker.

Openhab
https://www.openhab.org/

Home Assistant
https://www.home-assistant.io/

But it'll work with any HA system that can process and send MQTT / Json messages.

## Connecting to your stove
Connect to the Wifi of the stove
The pellet stove willl typically run at a designated ip address 192.168.120.1 (this is hard coded in the official app).
So a good place to start is setting up a device like a RPI connected to the Wifi of the stove.
Make sure you can ping the device at 192.168.120.1 before proceeding. 

## Docker Installation
It is possible to run maestrogateway inside a docker container. It requires the installation of docker and docker-compose. 
https://hub.docker.com/r/chibald/maestrogateway

1. Update docker-compose.yml as needed. See example below:
[Docker-compose](https://docs.docker.com/compose/install/) example:

```yaml
version: '3.3'
services:

  maestrogateway:
    image: chibald/maestrogateway:latest
    network_mode: host
    environment:      
      MQTT_ip: 'broker.hivemq.com'
      MQTT_port: 1883
      MQTT_authentication: 'False'
      MQTT_user: ''
      MQTT_pass: ''
      MQTT_TOPIC_SUB: 'Maestro/Command/'
      MQTT_TOPIC_PUB: 'Maestro/'
      MQTT_PAYLOAD_TYPE: 'TOPIC'
      WS_RECONNECTS_BEFORE_ALERT: 5
      MCZip: '192.168.120.1'
      MCZport: '81'

    restart: unless-stopped
```
2. Run `docker-compose up --detach` to build and start maestrogateway

## Script Installation (RPI) 
create a folder "maestro", in this folder run:

```sh
git clone https://github.com/Chibald/maestrogateway .
```

Open the config file and edit as neccesary
```sh
sudo nano _config_.py
```

For a normal installation and a test launch in console:
```sh
sudo bash install
```

For installation and use in daemon:
```sh
sudo bash install_daemon
```

To start the daemon
```sh
sudo systemctl start maestro.service
```

# Credits
This script is based on a script from Anthony L which you can find here.
https://github.com/Anthony-55/maestro

His version is made for Jeedom, a French HA system. The jeedom forum has got interesting topics about managing pellet stoves and heaters using Jeedom. ex.
https://community.jeedom.com/t/mcz-maestro-et-jeedom/6159

Also tharts and deSteini have contributed. If you like things changed, improved or added you're welcome to make a Pull Request.
