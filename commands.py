#coding: utf-8

'''
MCZ Maestro Command class
These are the supported commands to be set via websocket
'''

class MaestroCommand:
    def __init__(self, name, id, commandtype):
        self.name = name # Name in Json Command
        self.maestroid = id # Maestro command ID to be sent via websocket
        self.commandtype = commandtype # Command type

commands = []
commands.append(MaestroCommand('Temperature_Setpoint', 42, 'temperature'))
commands.append(MaestroCommand('Boiler_Setpoint', 51, 'temperature'))
commands.append(MaestroCommand('Chronostat', 1111, 'onoff'))
commands.append(MaestroCommand('Chronostat_T1', 1108, 'temperature'))
commands.append(MaestroCommand('Chronostat_T2', 1109, 'temperature'))
commands.append(MaestroCommand('Chronostat_T3', 1110, 'temperature'))
commands.append(MaestroCommand('Power_Level', 36, 'int'))
commands.append(MaestroCommand('Silent_Mode', 45, 'onoff'))
commands.append(MaestroCommand('Active_Mode', 35, 'onoff'))
commands.append(MaestroCommand('Eco_Mode', 41, 'onoff'))
commands.append(MaestroCommand('Sound_Effects', 50, 'onoff'))
commands.append(MaestroCommand('Power', 34, 'onoff40'))
commands.append(MaestroCommand('Fan_State', 37, 'int')) # 0, 1, 2, 3 ,4,  5 ,6 
commands.append(MaestroCommand('Refresh', 0, 'Refresh'))

def getMaestroCommand(commandname):
    i = 0
    while i < len(commands):
        if commandname == commands[i].name:
            return commands[i]    
        i += 1
    return MaestroCommand('Unknown', -1, 'Unknown')