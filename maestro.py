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

class PileFifo(object):
    def __init__(self,maxpile=None):
        self.pile=[]
        self.maxpile = maxpile

    def empile(self,element,idx=0):
        if (self.maxpile!=None) and (len(self.pile)==self.maxpile):
            raise ValueError ("erreur: tentative d'empiler dans une pile pleine")
        self.pile.insert(idx,element)
 
    def depile(self,idx=-1):
        if len(self.pile)==0:
            raise ValueError ("erreur: tentative de depiler une pile vide")
        if idx<-len(self.pile) or idx>=len(self.pile):
            raise ValueError ("erreur: element de pile à depiler n'existe pas")
        return self.pile.pop(idx)
 
    def element(self,idx=-1):
        if idx<-len(self.pile) or idx>=len(self.pile):
            raise ValueError ("erreur: element de pile à lire n'existe pas")
        return self.pile[idx]
 
    def copiepile(self,imin=0,imax=None):
        if imax==None:
            imax=len(self.pile)
        if imin<0 or imax>len(self.pile) or imin>=imax:
            raise ValueError ("erreur: mauvais indice(s) pour l'extraction par copiepile")
        return list(self.pile[imin:imax])
 
    def pilevide(self):
        return len(self.pile)==0
 
    def pilepleine(self):
        return self.maxpile!=None and len(self.pile)==self.maxpile
 
    def taille(self):
        return len(self.pile)

Message_MQTT=PileFifo()
Message_WS=PileFifo()

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

from _config_ import _MQTT_authentication
from _config_ import _MQTT_user
from _config_ import _MQTT_pass

MQTT_MAESTRO = {}

logger.info('Lancement du deamon')
logger.info('Anthony L. 2019')
logger.info('Niveau de LOG : DEBUG')


def on_connect_mqtt(client, userdata, flags, rc):
	logger.info("Connecté au broker MQTT avec le code : " + str(rc))

def on_message_mqtt(client, userdata, message):
	logger.info('Message MQTT reçu : ' + str(message.payload.decode()))
	cmd = message.payload.decode().split(",")
	if cmd[0] == "42":
		cmd[1]=(int(cmd[1])*2)
	Message_MQTT.empile("C|WriteParametri|"+cmd[0]+"|"+str(cmd[1]))
	logger.info('Contenu Pile Message_MQTT : ' + str(Message_MQTT.copiepile()))

def secTOdhms(nb_sec):
	qm,s=divmod(nb_sec,60)
	qh,m=divmod(qm,60)
	d,h=divmod(qh,24)
	return "%d:%d:%d:%d" %(d,h,m,s)
	
def on_message(ws, message):
	logger.info('Message sur le serveur websocket reçu : ' + str(message))
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
								MQTT_MAESTRO[RecuperoInfo[j][1]] = ('Code inconnu :', str(int(message.split("|")[i],16)))
					else:
						if i == 6 or i == 26 or i == 28:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = float(int(message.split("|")[i],16)/2)
						
						elif i >= 37 and i <=42:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = secTOdhms(int(message.split("|")[i],16))
						else:
							MQTT_MAESTRO[RecuperoInfo[j][1]] = int(message.split("|")[i],16)
	logger.info('Publication sur le topic MQTT ' + str(_MQTT_TOPIC_PUB) + ' le message suivant : ' + str(json.dumps(MQTT_MAESTRO)))
	client.publish(_MQTT_TOPIC_PUB, json.dumps(MQTT_MAESTRO),1)

def on_error(ws, error):
	logger.info(error)

def on_close(ws):
	logger.info('Session websocket fermée')

def on_open(ws):
	def run(*args):
		for i in range(_TEMPS_SESSION):
			time.sleep(_INTERVALLE)
			if Message_MQTT.pilevide():
				Message_MQTT.empile("C|RecuperoInfo")
			cmd = Message_MQTT.depile()
			logger.info("Envoi de la commande : " + str(cmd))
			ws.send(cmd)
		time.sleep(1)
		ws.close()
	thread.start_new_thread(run, ())

logger.info('Connection en cours au broker MQTT (IP:'+_MQTT_ip + ' PORT:'+str(_MQTT_port)+')')
client = mqtt.Client()
if _MQTT_authentication == True:
	client.username_pw_set(username=_MQTT_user,password=_MQTT_pass)
client.on_connect = on_connect_mqtt
client.on_message = on_message_mqtt
client.connect(_MQTT_ip, _MQTT_port)
client.loop_start()
logger.info('Souscription au topic ' + str(_MQTT_TOPIC_SUB) + ' avec un Qos=1')
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