[![Build](https://github.com/Chibald/MaestroGateway/workflows/Build/badge.svg)](https://github.com/Chibald/maestrogateway/actions?query=workflow%3ABuild)
[![Standalone](https://github.com/Chibald/MaestroGateway/workflows/Standalone/badge.svg)](https://github.com/Chibald/maestrogateway/actions?query=workflow%3AStandalone)
[![Daemon Service](https://github.com/Chibald/MaestroGateway/workflows/Daemon%20Service/badge.svg)](https://github.com/Chibald/maestrogateway/actions?query=workflow%3A%22Daemon+Service%22)

![Warning](https://github.com/Chibald/maestrogateway/blob/master/docs/disclaimer.png)


This is a script for relaying messages to a MCZ Maestro pellet stove. All of this software is provided AS-IS with no implied warranty or liability under sections 15, and 16 of the GPL V3. So if your stove burns down your house, it's not my fault.

# MCZ Maestro Equipment Gateway with Mqtt / JSON
Python script for controlling Pellet Stoves using Maestro technology.

It is known to work with newer pellet stoves from MZC
Personally I use it using a MCZ Musa Hydro stove.

## About Maestro
Maestro technology uses a Websocket to communicatie with the pellet stove. It is used by the MZC Maestro App and also by external thermostats.
https://www.mcz.it/en/maestro-technology/

## Usage
This script returns the websocket data in the form of a Json string on a MQTT topic which you can use in your home automation  software. You can use this information to display the state of all parameters from the stove.
Also all basic commands that you can send using the official MZC app are available on another MQTT topic.

### Recieving information
Every 15 seconds the maestro.service will post an update to the Mqtt topic.

```
{ "Stove_State": 0, "Fan_State": 1, "DuctedFan1": 0.0, "DuctedFan2": 0.0, "Fume_Temperature": 22.5, "Ambient_Temperature": 19.5, "Puffer_Temperature": 127.5, "Boiler_Temperature": 51.0, "NTC3_Temperature": 127.5, "Candle_Condition": 0, "ACTIVE_Set": 150, "RPM_Fam_Fume": 0, "RPM_WormWheel_Set": 0, "RPM_WormWheel_Live": 0, "3WayValve": "Risc", "Pump_PWM": 0, "Brazier": "OK", "Profile": 1, "Modbus_Address": 41, "Active_Mode": 1, "Active_Live": 99, "Control_Mode": 1, "ECO_Mode": 1, "Silent_Mode": 0, "Chrono_Mode": 1 
.....
```
the script will check if value has changed, so next messages are filtered for changes vakues only

for example:
```
{"Ambient_Temperature": 19.0}
```

### Sending commands
Publish Json command on the command Mqtt - topic to issue commands.
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

etc.
Check out the list in commands.py for available commands.


## Hardware Prerequisities
The MCZ pellet stove has its own Wifi SSID. The easiest way to bridge this connection is by using a Raspberry 3 with a wired ethernet to your lan, and to configure the onboard Wifi to connect to the SSID of the pellet stove. But any device with two lans will work.

## Software Prerequisities
You will need a Home Automation software with MQTT broker. Personally I use openHab and it works fine. 
https://www.openhab.org/

But it'll work with any HA system that can process and send MQTT / Json messages.
As this is a python script you'll also need python installed.

## Connecting to your stove
Connect to the Wifi of the stove
The pellet stove willl typically run at a designated ip address 192.168.120.1 (this is hard coded in the official app).
So a good place to start is setting up a device like a RPI connected to the Wifi of the stove.
Make sure you can ping the device before proceeding.

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

## Docker Installation
It is possible to run maestrogateway inside a docker container. It requires the installation of docker and docker-compose. 

If you are using a raspberry pi you can use the scripts from gcgarner/IOTStack to make installation easy.
https://github.com/gcgarner/IOTstack

### build the docker image
```
docker-compose build
```

### run the container 
```
docker-compose up -d
```

### stop the container
```
docker-compose down
```

## Updating:
!! Before updating, make a back up of your config file !!

```
cd maestro
git pull
```

if you are running maestrogateway as a local service:

```
sudo bash update_daemon
```

if you are running as docker container:

```
docker-compose build
docker-compose up -d
```

# Credits
This script is based on a script from Anthony L which you can find here.
https://github.com/Anthony-55/maestro

His version is made for Jeedom, a French HA system. The jeedom forum has got interesting topics about managing pellet stoves and heaters using Jeedom. ex.
https://community.jeedom.com/t/mcz-maestro-et-jeedom/6159
