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
from logging.handlers import RotatingFileHandler

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# MCZ MAESTRO
_IP_POELE = "192.168.120.1"
_PORT_POELE = "81"
_INTERVALLE = 1
_TEMPS_SESSION = 60

# MQTT
_IP_BROKER = "192.168.1.18"
_PORT_BROKER = 1883
_TOPIC_SUB = "jeedom2"
_TOPIC_PUB = "jeedom"
MQTT_MAESTRO = {}
cmd_mqtt = "C|RecuperoInfo"
bit_vie = False

logger.info('Démarrage en cours du script.')
logger.info('Anthony L. 2019')
logger.info('Niveau de LOG : DEBUG')


def on_connect_mqtt(client, userdata, flags, rc):
	logger.info("Connecté au broker MQTT avec le code", rc)

def on_message_mqtt(client, userdata, message):
	global cmd_mqtt
	logger.info('Message MQTT reçu :', message.payload.decode())
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

def info_deamon():
	os.system('cls' if os.name=='nt' else 'clear')
	print("Deamon MAESTRO en cours d'execution.")
	print()
	print("Informations de connection :")
	print("MAESTRO :")
	print("Relevé d'information sur ",_IP_POELE)
	print("Intervalle de référence :",_INTERVALLE)
	print("Temps d'une session : ",_TEMPS_SESSION)
	print("MQTT :")
	print("Publications des messages sur :",_IP_BROKER)
	print()
	print("Bit de vie :",bit_vie)
	
def on_message(ws, message):
	logger.info('Message sur le serveur websocket reçu :', message)
	global bit_vie
	global cmd_mqtt
	#info_deamon()
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
								MQTT_MAESTRO[RecuperoInfo[j][1]] = ("Code inconnu", str(int(message.split("|")[i],16)))
					else:
						if i == 6 or i == 26 or i == 28:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = int(message.split("|")[i],16)/2
						elif i >= 37 and i <=42:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = secTOdhms(int(message.split("|")[i],16))
						else:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = int(message.split("|")[i],16)
	logger.info('Publication sur le topic MQTT',_TOPIC_PUB,'le message suivant :', MQTT_MAESTRO)
	client.publish(_TOPIC_PUB, json.dumps(MQTT_MAESTRO),1)
	if cmd_mqtt != "C|RecuperoInfo":
		cmd_mqtt = "C|RecuperoInfo"
	bit_vie = not bit_vie

def on_error(ws, error):
	logger.info(error)

def on_close(ws):
	logger.info('Session websocket fermée')

def on_open(ws):
	def run(*args):
		for i in range(_TEMPS_SESSION):
			time.sleep(_INTERVALLE)
			logger.info("Envoi de la commande:",cmd_mqtt)
			ws.send(cmd_mqtt)
		time.sleep(1)
		ws.close()
	thread.start_new_thread(run, ())

logger.info('Connection en cours au broker MQTT (IP:'+_IP_BROKER,'PORT:'+_PORT_BROKER+')')
client = mqtt.Client()
client.on_connect = on_connect_mqtt
client.on_message = on_message_mqtt
client.connect(_IP_BROKER, _PORT_BROKER)
client.loop_start()
logger.info('Souscription au topic',_TOPIC_SUB,'avec un Qos=1')
client.subscribe(_TOPIC_SUB, qos=1)

if __name__ == "__main__":
	while True:
		logger.info("Etablissement d'une nouvelle connection au serveur websocket (IP:"+_IP_POELE,"PORT:"+_PORT_POELE+")")
		websocket.enableTrace(False)
		ws = websocket.WebSocketApp("ws://" + _IP_POELE + ":" + _PORT_POELE,
									on_message = on_message,
									on_error = on_error,
									on_close = on_close)
		ws.on_open = on_open
		ws.run_forever()
		time.sleep(_INTERVALLE)