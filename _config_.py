#coding: utf-8
'''
Edit as needed
'''
_MQTT_ip = '192.168.1.3'				# Adresse IP du broker mqtt
_MQTT_port = 1883						# Mqtt port
_MQTT_authentication = False            # Mqtt use authentication? 
_MQTT_user = ''			                # Mqtt User name
_MQTT_pass = ''			                # Mqtt password
_MQTT_TOPIC_SUB = 'SUBmcz'			    # Publish command messages here
_MQTT_TOPIC_PUB = 'PUBmcz'			    # Information messages by daemon are published here
_MCZip ='192.168.120.1'				    # Stove IP Address. This probably is always this address.
_MCZport = '81'						    # Port du serveur embarqué du poele
_VERSION = '1.0'					    # Version