#!/usr/bin/python3
# coding: utf-8
import socket
import struct
import paho.mqtt.client as mqtt
import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import logging
import threading
import datetime
from logging.handlers import RotatingFileHandler
from fifoqueue import PileFifo

# Intervals
wsInterval = 1
wsConnectionTime = 360
recuperoInfoInterval = 15.0

# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# MZC Stove Configuration
from _config_ import _MCZport
from _config_ import _MCZip

# Commands
from commands import MaestroCommand, getMaestroCommand, commands

# Messages
from messages import RecuperoInfo, MaestoMessage
Message_MQTT = PileFifo()
MaestroInfoMessageCache = {}

# MQTT
from _config_ import _MQTT_pass
from _config_ import _MQTT_user
from _config_ import _MQTT_authentication
from _config_ import _MQTT_TOPIC_PUB
from _config_ import _MQTT_TOPIC_SUB
from _config_ import _MQTT_port
from _config_ import _MQTT_ip

# Websocket
wsConnected = False

# Start
logger.info('Lancement du deamon, Chibald verzione')
logger.info('Forked from Anthony L.''s Maestro daemon.')


def on_connect_mqtt(client, userdata, flags, rc):
    logger.info("MQTT: Connected to broker. " + str(rc))


def on_message_mqtt(client, userdata, message):
    logger.info('MQTT: Message recieved: ' + str(message.payload.decode()))
    res = json.loads(str(message.payload.decode()))
    maestrocommand = getMaestroCommand(res["Command"])
    if maestrocommand.name == "Unknown":
        logger.info(
            'Unknown Maestro JSON Command Recieved. Ignoring.' + message)
    elif maestrocommand.name == "Refresh":
        logger.info('Clearing the message cache')
        MaestroInfoMessageCache.clear()
    else:
        write = "C|WriteParametri|"
        writevalue = float(res["Value"])
        if maestrocommand.commandtype == 'temperature':
            writevalue = int(writevalue*2)
        elif maestrocommand.commandtype == "onoff40":
            writevalue = int(writevalue)
            if writevalue == 0:
                writevalue = 40
            else:
                writevalue = 1
        elif maestrocommand.commandtype == "onoff":
            writevalue = int(writevalue)
            if writevalue != 1:
                writevalue = 0

        write += str(maestrocommand.maestroid) + "|" + str(writevalue)
        Message_MQTT.empile(write)


def secTOdhms(nb_sec):
    qm, s = divmod(nb_sec, 60)
    qh, m = divmod(qm, 60)
    d, h = divmod(qh, 24)
    return "%d:%d:%d:%d" % (d, h, m, s)


def RecuperoInfo_EnQueue():
    threading.Timer(recuperoInfoInterval, RecuperoInfo_EnQueue).start()
    if wsConnected:
        Message_MQTT.empile("C|RecuperoInfo")


def ProcessRecuperoInfo(message):
    res = {}
    MaestroInfoMessagePub = {}
    for i in range(1, len(message.split("|"))):
        found = False
        for j in range(0, len(RecuperoInfo)):
            if i == RecuperoInfo[j][0]:
                if i == 6 or i == 26 or i == 28 or i == 8 or i == 27:  # Temperatures are divided by 2
                    res[RecuperoInfo[j][1]] = float(
                        int(message.split("|")[i], 16))/2
                    found = True
                elif i >= 37 and i <= 42:
                    res[RecuperoInfo[j][1]] = secTOdhms(
                        int(message.split("|")[i], 16))
                    found = True
                else:
                    res[RecuperoInfo[j][1]] = int(message.split("|")[i], 16)
                    found = True
        if found == False:
            res['Unknown'+str(i)] = int(message.split("|")[i], 16)

    for item in res:
        if item not in MaestroInfoMessageCache:
            MaestroInfoMessageCache[item] = res[item]
            MaestroInfoMessagePub[item] = res[item]
        elif MaestroInfoMessageCache[item] != res[item]:
            MaestroInfoMessageCache[item] = res[item]
            MaestroInfoMessagePub[item] = res[item]

    if len(MaestroInfoMessagePub) == 0:
        MaestroInfoMessagePub["Status"] = "No Changes"

    logger.info('MQTT: publish to Topic "' + str(_MQTT_TOPIC_PUB) +
                '", Message : ' + str(json.dumps(MaestroInfoMessagePub)))
    client.publish(_MQTT_TOPIC_PUB, json.dumps(MaestroInfoMessagePub), 1)


def on_message(ws, message):
    messageArray = message.split("|")
    if messageArray[0] == MaestoMessage.Info.value:
        ProcessRecuperoInfo(message)
    elif messageArray[0] == MaestoMessage.Ping.value:
        Message_MQTT.empile("P|PONG")
    else:
        logger.info('Unsupported message type recieved !')


def on_error(ws, error):
    logger.info(error)


def on_close(ws):
    logger.info('Websocket: Disconnected')
    global wsConnected
    wsConnected = False


def on_open(ws):
    logger.info('Websocket: Connected')
    global wsConnected
    wsConnected = True

    def run(*args):
        for i in range(wsConnectionTime*4):
            time.sleep(wsInterval/4)
            if Message_MQTT.pilevide() == False:
                cmd = Message_MQTT.depile()
                logger.info("Websocket: Send " + str(cmd))
                ws.send(cmd)
        logger.info('Closing Websocket Connection')
        ws.close()
    thread.start_new_thread(run, ())


logger.info('Connection in progress to the MQTT broker (IP:' +
            _MQTT_ip + ' PORT:'+str(_MQTT_port)+')')
client = mqtt.Client()
if _MQTT_authentication:
    client.username_pw_set(username=_MQTT_user, password=_MQTT_pass)
client.on_connect = on_connect_mqtt
client.on_message = on_message_mqtt
client.connect(_MQTT_ip, _MQTT_port)
client.loop_start()
logger.info('MQTT: Subscribed to topic "' + str(_MQTT_TOPIC_SUB) + '"')
client.subscribe(_MQTT_TOPIC_SUB, qos=1)

if __name__ == "__main__":
    RecuperoInfo_EnQueue()
    mep = 0
    while mep < 1:
        logger.info(
            "Websocket: Establishing connection to server (IP:"+_MCZip+" PORT:"+_MCZport+")")
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp("ws://" + _MCZip + ":" + _MCZport,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open

        ws.run_forever(ping_interval=5, ping_timeout=2)
        time.sleep(wsInterval)

        mep = mep + 1
        logger.info(mep)
