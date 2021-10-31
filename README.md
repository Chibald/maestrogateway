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

After version 1.03 it's also possible to send diagnostics commands. For these commands you first have to put the stove in diagnostics mode. You can only put the stove in diagnostic mode when the stove is powered off. Diagnostic mode enables you to control some stove parameters that are normally not available. A use case is to control the 3 walve valve / water pump to get heat from a boiler. See commands.py for command list.

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
{"Stove_State": 11, "Power": 1, "Diagnostics": 0, "Fan_State": 1, "DuctedFan1": 0, "DuctedFan2": 0, "Fume_Temperature": 155, "Ambient_Temperature": 23.5, "Puffer_Temperature": 127.5, "Boiler_Temperature": 62.5, "NTC3_Temperature": 127.5, "Candle_Condition": 0, "ACTIVE_Set": 156, "RPM_Fam_Fume": 708, "RPM_WormWheel_Set": 150, "RPM_WormWheel_Live": 300, "3WayValve": "Risc", "Pump_PWM": 100, "Brazier": "OK", "Profile": 0, "Modbus_Address": 11, "Active_Mode": 1, "Active_Live": 157, "Control_Mode": 1, "Eco_Mode": 0, "Silent_Mode": 1, "Chronostat": 0, "Temperature_Setpoint": 23.5, "Boiler_Setpoint": 80.0, "Temperature_Motherboard": 37.5, "Power_Level": 11, "FirmwareVersion": 68107, "DatabaseID": 28, "Date_Time_Hours": 14, "Date_Time_Minutes": 39, "Date_Day_Of_Month": 31, "Date_Month": 10, "Date_Year": 2021, "Total_Operating_Hours": "307:00:03", "Hours_Of_Operation_In_Power1": "194:18:37", "Hours_Of_Operation_In_Power2": "0:32:50", "Hours_Of_Operation_In_Power3": "0:34:39", "Hours_Of_Operation_In_Power4": "0:34:45", "Hours_Of_Operation_In_Power5": "22:31:17", "Hours_To_Service": 1692, "Minutes_To_Switch_Off": 212, "Number_Of_Ignitions": 170, "Active_Temperature": 0, "Celcius_Or_Fahrenheit": 0, "Sound_Effects": 0, "Sound_Effects_State": 0, "Sleep": 0, "Mode": 0, "WifiSondeTemperature1": 255, "WifiSondeTemperature2": 255, "WifiSondeTemperature3": 255, "Unknown": 255, "SetPuffer": 130, "SetBoiler": 100, "SetHealth": 255, "Return_Temperature": 127.5, "AntiFreeze": 0}
.....

```
the script will check if value has changed to prevent message flooding, so next messages are filtered for changes values only

for example:
```
{"Ambient_Temperature": 19.0}
```

#### Payload type topic
If you use payload type Topic, all the parameters will be published to a separate topic under the `MQTT_TOPIC_PUB` topic for example
```
Maestro/Status/Ambient_Temperature, 19.0
```

| Topic | Description |
| ----------------------- | ----------- |
| Maestro/Power | Current power state (on / off)
| Maestro/Command/Power | Turn stove on or off 
| Maestro/Diagnostics | Current diagnostics state
| Maestro/Command/Diagnostics | Set stove in diagnostics mode. Can only be set to diagnostics mode when stove is powered off.
| Maestro/Command/Refresh | Clear the maestrogateway's message cache
| Maestro/Command/GetInfo | Get stove info immediately (instead of waiting till next cycle)
| Maestro/state |
| Maestro/Stove_State |
| Maestro/Fan_State |
| Maestro/Command/Fan_State |
| Maestro/DuctedFan1 |
| Maestro/Command/DuctedFan1 |
| Maestro/DuctedFan2 |
| Maestro/Command/DuctedFan2 |
| Maestro/Fume_Temperature |
| Maestro/Ambient_Temperature |
| Maestro/Puffer_Temperature |
| Maestro/Boiler_Temperature |
| Maestro/NTC3_Temperature |
| Maestro/Candle_Condition |
| Maestro/ACTIVE_Set |
| Maestro/RPM_Fam_Fume |
| Maestro/RPM_WormWheel_Set |
| Maestro/RPM_WormWheel_Live |
| Maestro/3WayValve |
| Maestro/Command/3WayValve | 
| Maestro/Pump_PWM | current pumping speed (percentage)
| Maestro/Command/Pump_PWM | Turn on the water pump. This only works when stove is in diagnostics mode
| Maestro/Brazier |
| Maestro/Profile |
| Maestro/Modbus_Address |
| Maestro/Active_Mode |
| Maestro/Command/Active_Mode |
| Maestro/Active_Live |
| Maestro/Control_Mode |
| Maestro/Command/Control_Mode |
| Maestro/Eco_Mode |
| Maestro/Command/Eco_Mode |
| Maestro/Silent_Mode |
| Maestro/Command/Silent_Mode |
| Maestro/Chronostat |
| Maestro/Command/Chronostat |
| Maestro/Temperature_Setpoint |
| Maestro/Command/Temperature_Setpoint |
| Maestro/Boiler_Setpoint |
| Maestro/Command/Boiler_Setpoint |
| Maestro/Temperature_Motherboard |
| Maestro/Power_Level |
| Maestro/Command/Power_Level |
| Maestro/FirmwareVersion |
| Maestro/DatabaseID |
| Maestro/Date_Time_Hours |
| Maestro/Date_Time_Minutes |
| Maestro/Date_Day_Of_Month |
| Maestro/Date_Month |
| Maestro/Date_Year |
| Maestro/Total_Operating_Hours |
| Maestro/Hours_Of_Operation_In_Power1 |
| Maestro/Hours_Of_Operation_In_Power2 |
| Maestro/Hours_Of_Operation_In_Power3 |
| Maestro/Hours_Of_Operation_In_Power4 |
| Maestro/Hours_Of_Operation_In_Power5 |
| Maestro/Hours_To_Service |
| Maestro/Minutes_To_Switch_Off |
| Maestro/Number_Of_Ignitions |
| Maestro/Active_Temperature |
| Maestro/Celcius_Or_Fahrenheit |
| Maestro/Sound_Effects |
| Maestro/Command/Sound_Effects |
| Maestro/Sleep |
| Maestro/Mode |
| Maestro/WifiSondeTemperature1 |
| Maestro/WifiSondeTemperature2 |
| Maestro/WifiSondeTemperature3 |
| Maestro/SetPuffer |
| Maestro/SetBoiler |
| Maestro/SetHealth |
| Maestro/Return_Temperature |
| Maestro/AntiFreeze |
| Maestro/Command/Chronostat_T1 |
| Maestro/Command/Chronostat_T2 |
| Maestro/Command/Chronostat_T3 |

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
Maestro/Command/Power, 1
```

to turn off the stove:
```
Maestro/Command/Power, 0
```

to set temperature to 20.5 degrees:
```
Maestro/Command/Temperature_Setpoint, 20.5
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
