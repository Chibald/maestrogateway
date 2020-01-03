.. image:: https://github.com/Chibald/Maestro/blob/openhab_compatibility/docs/disclaimer.png
This is a script for relaying messages to a MZC Maestro pellet stove. All of this software is provided AS-IS with no implied warranty or liability under sections 15, and 16 of the GPL V3. So if your stove burns down your house, it's not my fault.

# MCZ Maestro Equipment Gateway with Mqtt / JSON
Python script for controlling Pellet Stoves using Maestro technology.

It is known to work with newer pellet stoves from MZC
Personally I use it using a MZC Musa Hydro stove.

## About Maestro
Maestro technology uses a Websocket to communicatie with the pellet stove. It is used by the MZC Maestro App and also by external thermostats.
https://www.mcz.it/en/maestro-technology/

## Usage
This script returns the websocket data in the form of a Json string on a MQTT topic which you can use in your home automation  software. You can use this information to display the state of all parameters from the stove.
Also all basic commands that you can send using the official MZC app are available on another MQTT topic.

### Recieving information
Every 15 seconds the maestro.service will post an update to the Mqtt topic.

### Sending commands
Publish Json command on the command Mqtt - topic to issue commands.
For example, to turn on the stove or to turn off the stove.

## Hardware Prerequisities
The MZC pellet stove has its own Wifi SSID. The easiest way to bridge this connection is by using a Raspberry 3 with a wired ethernet to your lan, and to configure the onboard Wifi to connect to the SSID of the pellet stove. But any device with two lans will work.

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
create a folder, in this folder run:

```sh
git clone --single-branch --branch openhab_compatibility https://github.com/Chibald/Maestro.git .
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

## Updating:
```sh
cd maestro
git pull
sudo bash update_daemon
```

# Credits
This script is based on a script from Anthony L which you can find here.
https://github.com/Anthony-55/maestro


His version is made for Jeedom, a French HA system. The jeedom forum has got interesting topics about managing pellet stoves and heaters using Jeedom. ex.
https://community.jeedom.com/t/mcz-maestro-et-jeedom/6159
