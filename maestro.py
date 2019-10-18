#!/usr/bin/python3
#coding: utf-8

import paho.mqtt.client as mqtt
import websocket
try:
	import thread
except ImportError:
	import _thread as thread
import time
import sys
import os
import json
import logging
import datetime
from logging.handlers import RotatingFileHandler

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

# MCZ MAESTRO
from _config_ import _MCZip
from _config_ import _MCZport
_INTERVALLE = 1
_TEMPS_SESSION = 60

# MQTT
from _config_ import _MQTT_ip
from _config_ import _MQTT_port
from _config_ import _MQTT_TOPIC_SUB
from _config_ import _MQTT_TOPIC_PUB
MQTT_MAESTRO = {}
cmd_mqtt = "C|RecuperoInfo"
bit_vie = False

logger.info('Lancement du deamon')
logger.info('Anthony L. 2019')
logger.info('Niveau de LOG : DEBUG')


def on_connect_mqtt(client, userdata, flags, rc):
	logger.info("Connecté au broker MQTT avec le code : " + rc)

def on_message_mqtt(client, userdata, message):
	global cmd_mqtt
	logger.info('Message MQTT reçu : ' + message.payload.decode())
	cmd_mqtt = message.payload.decode()
	cmd_mqtt = cmd_mqtt.split(",")
	if cmd_mqtt[0]=="42":
		cmd_mqtt[1]=(int(cmd_mqtt[1])*2)
	cmd_mqtt = "C|WriteParametri|"+cmd_mqtt[0]+"|"+str(cmd_mqtt[1])

def secTOdhms(nb_sec):
	qm,s=divmod(nb_sec,60)
	qh,m=divmod(qm,60)
	d,h=divmod(qh,24)
	return "%d:%d:%d:%d" %(d,h,m,s)
	
def on_message(ws, message):
	logger.info('Message sur le serveur websocket reçu : ' + message)
	global cmd_mqtt
	from _data_ import RecuperoInfo
	for i in range(0,len(message.split("|"))):
			for j in range(0,len(RecuperoInfo)):
				if i == RecuperoInfo[j][0]:
					if len(RecuperoInfo[j]) > 2:
						for k in range(0,len(RecuperoInfo[j][2])):
							if int(message.split("|")[i],16) == RecuperoInfo[j][2][k][0]:
								MQTT_MAESTRO[RecuperoInfo[j][1]] = RecuperoInfo[j][2][k][1]
								break
							else:
								MQTT_MAESTRO[RecuperoInfo[j][1]] = ('Code inconnu', str(int(message.split("|")[i],16)))
					else:
						if i == 6 or i == 26 or i == 28:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = int(message.split("|")[i],16)/2
						'''
						elif i == 32:
							#Heure du poêle
							date = datetime.datetime.now()
							if int(message.split("|")[i],16) != date.hour:
								cmd_mqtt = "C|SalvaDataOra|"+str("%02d" %date.day)+str("%02d" %date.month)+str("%02d" %date.year)+str("%02d" %date.hour)+str("%02d" %date.minute)
						elif i == 33:
							#Minutes du poêle
							date= datetime.datetime.now()
							if int(message.split("|")[i],16) != date.minute:
								cmd_mqtt = "C|SalvaDataOra|"+str("%02d" %date.day)+str("%02d" %date.month)+str("%02d" %date.year)+str("%02d" %date.hour)+str("%02d" %date.minute)
						elif i == 34:
							#Jour du poêle
							date= datetime.datetime.now()
							if int(message.split("|")[i],16) != date.day:
								cmd_mqtt = "C|SalvaDataOra|"+str("%02d" %date.day)+str("%02d" %date.month)+str("%02d" %date.year)+str("%02d" %date.hour)+str("%02d" %date.minute)
						elif i == 35:
							#Mois du poêle
							date= datetime.datetime.now()
							if int(message.split("|")[i],16) != date.month:
								cmd_mqtt = "C|SalvaDataOra|"+str("%02d" %date.day)+str("%02d" %date.month)+str("%02d" %date.year)+str("%02d" %date.hour)+str("%02d" %date.minute)
												
						'''		
						elif i >= 37 and i <=42:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = secTOdhms(int(message.split("|")[i],16))
						else:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = int(message.split("|")[i],16)
	logger.info('Publication sur le topic MQTT ' + _MQTT_TOPIC_PUB + ' le message suivant : ' + json.dumps(MQTT_MAESTRO))
	client.publish(_MQTT_TOPIC_PUB, json.dumps(MQTT_MAESTRO),1)
	if cmd_mqtt != "C|RecuperoInfo":
		cmd_mqtt = "C|RecuperoInfo"


def on_error(ws, error):
	logger.info(error)

def on_close(ws):
	logger.info('Session websocket fermée')

def on_open(ws):
	def run(*args):
		for i in range(_TEMPS_SESSION):
			time.sleep(_INTERVALLE)
			logger.info("Envoi de la commande : " + cmd_mqtt)
			ws.send(cmd_mqtt)
		time.sleep(1)
		ws.close()
	thread.start_new_thread(run, ())

logger.info('Connection en cours au broker MQTT (IP:'+_MQTT_ip + ' PORT:'+str(_MQTT_port)+')')
client = mqtt.Client()
client.on_connect = on_connect_mqtt
client.on_message = on_message_mqtt
client.connect(_MQTT_ip, _MQTT_port)
client.loop_start()
logger.info('Souscription au topic ' + _MQTT_TOPIC_SUB + ' avec un Qos=1')
client.subscribe(_MQTT_TOPIC_SUB, qos=1)

if __name__ == "__main__":
	while True:
		logger.info("Etablissement d'une nouvelle connection au serveur websocket (IP:"+_MCZip+" PORT:"+_MCZport+")")
		websocket.enableTrace(False)
		ws = websocket.WebSocketApp("ws://" + _MCZip + ":" + _MCZport,
									on_message = on_message,
									on_error = on_error,
									on_close = on_close)
		ws.on_open = on_open
		ws.run_forever()
		time.sleep(_INTERVALLE)