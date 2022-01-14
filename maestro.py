#!/usr/bin/python3
# coding: utf-8
print("Starting Maestrogateway.")

import time
import sys
import os

systemd_available = True
try:
    import systemd
    from systemd.journal import JournalHandler
    from systemd import daemon
    import psutil, os
except:
  print("Systemd is not available. This is the case on docker alpine images and on windows machines")
  systemd_available = False

import json
import logging
import threading
import paho.mqtt.client as mqtt
import websocket

from logging.handlers import RotatingFileHandler
from messages import MaestroMessageType, process_infostring, get_maestro_info, get_maestro_infoname, MAESTRO_INFORMATION, MaestroInformation

from _config_ import _MCZport
from _config_ import _MCZip
from _config_ import _MQTT_pass
from _config_ import _MQTT_user
from _config_ import _MQTT_authentication
from _config_ import _MQTT_TOPIC_PUB, _MQTT_TOPIC_SUB, _MQTT_PAYLOAD_TYPE
from _config_ import _WS_RECONNECTS_BEFORE_ALERT
from _config_ import _MQTT_port
from _config_ import _MQTT_ip
from _config_ import _VERSION

from commands import MaestroCommand, get_maestro_command, maestrocommandvalue_to_websocket_string, MaestroCommandValue, MAESTRO_COMMANDS

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
                val.value = item.value
        if not found:
            queue.Queue._put(self, item)
            self.all_items.add(item)

    def _get(self):
        item = queue.Queue._get(self)
        self.all_items.remove(item)
        return item

get_stove_info_interval = 15.0
websocket_connected = False
socket_reconnect_count = 0
client = None
old_connection_status = None

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
if systemd_available and psutil.Process(os.getpid()).ppid() == 1:
    # We are using systemd
    journald_handler=JournalHandler()
    logger.addHandler(journald_handler)
else:
    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

CommandQueue = SetQueue()
MaestroInfoMessageCache = {}

# Start
logger.info('Starting Maestro Daemon')

def on_connect_mqtt(client, userdata, flags, rc):
    logger.info("MQTT: Connected to broker. " + str(rc))

def on_message_mqtt(client, userdata, message):
    try:
        maestrocommand = None
        cmd_value = None
        payload = str(message.payload.decode())
        if _MQTT_PAYLOAD_TYPE == 'TOPIC':
            topic = str(message.topic)
            command = topic[str(topic).rindex('/')+1:]
            logger.info(f"Command topic received: {topic}")
            maestrocommand = get_maestro_command(command)
            cmd_value = payload
        else:
            logger.info(f"MQTT: Message received: {payload}")
            res = json.loads(payload)
            maestrocommand = get_maestro_command(res["Command"])
            cmd_value = res["Value"]
        if maestrocommand.name == "Unknown":
            logger.info(f"Unknown Maestro Command Received. Ignoring. {payload}")
        elif maestrocommand.name == "Refresh":
            logger.info('Clearing the message cache')
            MaestroInfoMessageCache.clear()
        else:
            logger.info('Queueing Command ' + maestrocommand.name + ' ' + str(payload))
            CommandQueue.put(MaestroCommandValue(maestrocommand, cmd_value))
    except Exception as e: # work on python 3.x
            logger.error('Exception in on_message_mqtt: '+ str(e))

def recuperoinfo_enqueue():
    """Get Stove information every x seconds as long as there is a websocket connection"""
    threading.Timer(get_stove_info_interval, recuperoinfo_enqueue).start()
    if websocket_connected:
        CommandQueue.put(MaestroCommandValue(MaestroCommand('GetInfo', 0, 'GetInfo', 'GetInfo'), 0))
        client.publish(_MQTT_TOPIC_PUB + 'state',  'ON',  1)    

def send_connection_status_message(message):
    global old_connection_status
    if old_connection_status != message:
        if _MQTT_PAYLOAD_TYPE == 'TOPIC':
            json_dictionary = json.loads(str(json.dumps(message)))
            for key in json_dictionary:
                logger.info('MQTT: publish to Topic "' + str(_MQTT_TOPIC_PUB + key) +
                        '", Message : ' + str(json_dictionary[key]))
                client.publish(_MQTT_TOPIC_PUB+'/'+key, json_dictionary[key], 1)
        else:
            client.publish(_MQTT_TOPIC_PUB, json.dumps(message), 1)
        old_connection_status = message

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

    if len(maestro_info_message_publish) > 0:
        if _MQTT_PAYLOAD_TYPE == 'TOPIC':
            logger.info(str(json.dumps(maestro_info_message_publish)))
            for key in maestro_info_message_publish:
                logger.info('MQTT: publish to Topic "' + str(_MQTT_TOPIC_PUB + key) +'", Message : ' + str(maestro_info_message_publish[key]))
                client.publish(_MQTT_TOPIC_PUB + key, maestro_info_message_publish[key], 1)
        else:
            client.publish(_MQTT_TOPIC_PUB, json.dumps(maestro_info_message_publish), 1)


def on_message(ws, message):
    message_array = message.split("|")
    if message_array[0] == MaestroMessageType.Info.value:
        process_info_message(message)
    else:
        logger.info('Unsupported message type received !')

def on_error(ws, error):
    logger.info(error)

def on_close(ws):
    logger.info('Websocket: Disconnected')
    global websocket_connected
    websocket_connected = False

def on_open(ws):
    logger.info('Websocket: Connected')
    send_connection_status_message({"Status":"connected"})
    global websocket_connected
    websocket_connected = True
    socket_reconnect_count = 0
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

def start_mqtt():
    global client
    logger.info('Connection in progress to the MQTT broker (IP:' +
                _MQTT_ip + ' PORT:'+str(_MQTT_port)+')')
    client = mqtt.Client()
    if _MQTT_authentication:
        print('mqtt authentication enabled')
        client.username_pw_set(username=_MQTT_user, password=_MQTT_pass)
    client.on_connect = on_connect_mqtt
    client.on_message = on_message_mqtt
    client.connect(_MQTT_ip, _MQTT_port)
    client.loop_start()
    if _MQTT_PAYLOAD_TYPE == 'TOPIC':
        logger.info('MQTT: Subscribed to topic "' + str(_MQTT_TOPIC_SUB) + '#"')
        client.subscribe(_MQTT_TOPIC_SUB+'#', qos=1)
        publish_availabletopics()
    else:
        logger.info('MQTT: Subscribed to topic "' + str(_MQTT_TOPIC_SUB) + '"')
        client.subscribe(_MQTT_TOPIC_SUB, qos=1)   

def publish_availabletopics():  
    logger.info(_MQTT_TOPIC_PUB + 'state')  
    # Publish topics that have stat and command
    for item in MAESTRO_INFORMATION:
        logger.info(_MQTT_TOPIC_PUB + item.name)        
        maestrocommand = get_maestro_command(item.name)        
        if maestrocommand.name != "Unknown":
            logger.info(_MQTT_TOPIC_SUB + item.name)  

    # publish topics that have command only
    for item in MAESTRO_COMMANDS:
        homeassistanttype = 'sensor'   
        maestroinfo = get_maestro_infoname(item.name)
        if maestroinfo.name == "Unknown":
            logger.info(_MQTT_TOPIC_SUB + item.name) 

def init_config():
    print('Reading config from envionment variables')
    if (os.getenv('MQTT_ip') != None):
        global _MQTT_ip
        _MQTT_ip = os.getenv('MQTT_ip')
    if (os.getenv('MQTT_port') != None):
        global _MQTT_port
        _MQTT_port = int(os.getenv('MQTT_port'))
    if (os.getenv('MQTT_authentication') != None):
        global _MQTT_authentication
        _MQTT_authentication = os.getenv('MQTT_authentication') == "True"
    if (os.getenv('MQTT_user') != None):
        global _MQTT_user
        _MQTT_user = os.getenv('MQTT_user')
    if (os.getenv('MQTT_pass') != None):
        global _MQTT_pass
        _MQTT_pass = os.getenv('MQTT_pass')
    if (os.getenv('MQTT_TOPIC_PUB') != None):
        global _MQTT_TOPIC_PUB
        _MQTT_TOPIC_PUB = os.getenv('MQTT_TOPIC_PUB')
    if (os.getenv('MQTT_TOPIC_SUB') != None):
        global _MQTT_TOPIC_SUB
        _MQTT_TOPIC_SUB = os.getenv('MQTT_TOPIC_SUB')
    if (os.getenv('MQTT_PAYLOAD_TYPE') != None):
        global _MQTT_PAYLOAD_TYPE
        _MQTT_PAYLOAD_TYPE = os.getenv('MQTT_PAYLOAD_TYPE')
    if (os.getenv('WS_RECONNECTS_BEFORE_ALERT') != None):
        global _WS_RECONNECTS_BEFORE_ALERT
        _WS_RECONNECTS_BEFORE_ALERT = int(os.getenv('WS_RECONNECTS_BEFORE_ALERT'))
    if (os.getenv('MCZip') != None):
        global _MCZip
        _MCZip = os.getenv('MCZip')
    if (os.getenv('MCZport') != None):
        global _MCZport
        _MCZport = os.getenv('MCZport')
    
if __name__ == "__main__":
    init_config()        
    recuperoinfo_enqueue()
    socket_reconnect_count = 0
    start_mqtt()
    if systemd_available:
        systemd.daemon.notify('READY=1')
    while True:
        logger.info("Websocket: Establishing connection to server (IP:"+_MCZip+" PORT:"+_MCZport+")")
        ws = websocket.WebSocketApp("ws://" + _MCZip + ":" + _MCZport,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open

        ws.run_forever(ping_interval=5, ping_timeout=2, suppress_origin=True)
        time.sleep(1)
        socket_reconnect_count = socket_reconnect_count + 1
        logger.info("Socket Reconnection Count: " + str(socket_reconnect_count))
        if socket_reconnect_count>_WS_RECONNECTS_BEFORE_ALERT:
            send_connection_status_message({"Status":"disconnected"})
            socket_reconnect_count = 0
