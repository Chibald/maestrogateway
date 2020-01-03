#!/usr/bin/python3
# coding: utf-8
import time
import json
import logging
import threading

from logging.handlers import RotatingFileHandler
from _config_ import _MCZport
from _config_ import _MCZip
from messages import MaestroMessageType, process_infostring
from _config_ import _MQTT_pass
from _config_ import _MQTT_user
from _config_ import _MQTT_authentication
from _config_ import _MQTT_TOPIC_PUB
from _config_ import _MQTT_TOPIC_SUB
from _config_ import _MQTT_port
from _config_ import _MQTT_ip
from commands import MaestroCommand, get_maestro_command, maestrocommandvalue_to_websocket_string, MaestroCommandValue

import paho.mqtt.client as mqtt
import websocket

try:
    import thread
except ImportError:
    import _thread as thread

try:
    import queue
except ImportError:
    import Queue as queue

class SetQueue(queue.Queue):
    """ De-Duplicate message queue to prevent flipping values (Debounce) """
    def _init(self, maxsize):
        queue.Queue._init(self, maxsize)
        self.all_items = set()

    def _put(self, item):
        found = False
        for val in self.all_items:
            if val.command.name == item.command.name:
                found = True
                val.command.value = item.command.value
        if not found:
            queue.Queue._put(self, item)
            self.all_items.add(item)

    def _get(self):
        item = queue.Queue._get(self)
        self.all_items.remove(item)
        return item

GETSTOVEINFO_INTERVAL = 15.0
WEBSOCKET_CONNECTED = False

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

CommandQueue = SetQueue()
MaestroInfoMessageCache = {}

# Start
logger.info('Starting Maestro Daemon')

def on_connect_mqtt(client, userdata, flags, rc):
    logger.info("MQTT: Connected to broker. " + str(rc))

def on_message_mqtt(client, userdata, message):
    logger.info('MQTT: Message recieved: ' + str(message.payload.decode()))
    res = json.loads(str(message.payload.decode()))
    maestrocommand = get_maestro_command(res["Command"])
    if maestrocommand.name == "Unknown":
        logger.info('Unknown Maestro JSON Command Recieved. Ignoring.' + message)
    elif maestrocommand.name == "Refresh":
        logger.info('Clearing the message cache')
        MaestroInfoMessageCache.clear()
    else:
        CommandQueue.put(MaestroCommandValue(maestrocommand, float(res["Value"])))

def recuperoinfo_enqueue():
    """Get Stove information every x seconds as long as there is a websocket connection"""
    threading.Timer(GETSTOVEINFO_INTERVAL, recuperoinfo_enqueue).start()
    if WEBSOCKET_CONNECTED:
        CommandQueue.put(MaestroCommandValue(MaestroCommand('GetInfo', 0, 'GetInfo'), 0))

def process_info_message(message):
    """Process websocket array string that has the stove Info message"""
    res = process_infostring(message)
    maestro_info_message_publish = {}
        
    for item in res:
        if item not in MaestroInfoMessageCache:
            MaestroInfoMessageCache[item] = res[item]
            maestro_info_message_publish[item] = res[item]
        elif MaestroInfoMessageCache[item] != res[item]:
            MaestroInfoMessageCache[item] = res[item]
            maestro_info_message_publish[item] = res[item]

    if len(maestro_info_message_publish) == 0:
        maestro_info_message_publish["Status"] = "No Changes"

    logger.info('MQTT: publish to Topic "' + str(_MQTT_TOPIC_PUB) +
                '", Message : ' + str(json.dumps(maestro_info_message_publish)))

    client.publish(_MQTT_TOPIC_PUB, json.dumps(maestro_info_message_publish), 1)


def on_message(ws, message):
    message_array = message.split("|")
    if message_array[0] == MaestroMessageType.Info.value:
        process_info_message(message)
    else:
        logger.info('Unsupported message type recieved !')

def on_error(ws, error):
    logger.info(error)

def on_close(ws):
    logger.info('Websocket: Disconnected')
    global WEBSOCKET_CONNECTED
    WEBSOCKET_CONNECTED = False

def on_open(ws):
    logger.info('Websocket: Connected')
    global WEBSOCKET_CONNECTED
    WEBSOCKET_CONNECTED = True
    def run(*args):
        for i in range(360*4):
            time.sleep(0.25)
            while not CommandQueue.empty():
                cmd = maestrocommandvalue_to_websocket_string(CommandQueue.get())
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
    recuperoinfo_enqueue()
    SOCKET_RECONNECTED_COUNT = 0
    while SOCKET_RECONNECTED_COUNT < 1:
        try:
            logger.info("Websocket: Establishing connection to server (IP:"+_MCZip+" PORT:"+_MCZport+")")
            websocket.enableTrace(False)
            ws = websocket.WebSocketApp("ws://" + _MCZip + ":" + _MCZport,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.on_open = on_open

            ws.run_forever(ping_interval=5, ping_timeout=2)
            time.sleep(1)
            SOCKET_RECONNECTED_COUNT = SOCKET_RECONNECTED_COUNT + 1
            logger.info("Socket Connection Count: " + str(SOCKET_RECONNECTED_COUNT))
        except:
            pass
