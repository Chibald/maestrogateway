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

def on_connect_mqtt(client, userdata, flags, rc):
	print("Connected With Result Code "+rc)

def on_message_mqtt(client, userdata, message):
	global cmd_mqtt
	#print("Message Recieved: "+message.payload.decode())
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
	global bit_vie
	global cmd_mqtt
	info_deamon()
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
	client.publish(_TOPIC_PUB, json.dumps(MQTT_MAESTRO),1)
	if cmd_mqtt != "C|RecuperoInfo":
		cmd_mqtt = "C|RecuperoInfo"
	bit_vie = not bit_vie

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")

def on_open(ws):
	def run(*args):
		for i in range(_TEMPS_SESSION):
			time.sleep(_INTERVALLE)
			#print("Envoi de la commande:",cmd_mqtt)
			ws.send(cmd_mqtt)
		time.sleep(1)
		ws.close()
		print("thread terminating...")
	thread.start_new_thread(run, ())

client = mqtt.Client()
client.on_connect = on_connect_mqtt
client.on_message = on_message_mqtt
client.connect(_IP_BROKER, _PORT_BROKER)
client.loop_start()
client.subscribe(_TOPIC_SUB, qos=1)

if __name__ == "__main__":
	while True:
		websocket.enableTrace(False)
		ws = websocket.WebSocketApp("ws://" + _IP_POELE + ":" + _PORT_POELE,
									on_message = on_message,
									on_error = on_error,
									on_close = on_close)
		ws.on_open = on_open
		ws.run_forever()
		time.sleep(_INTERVALLE)