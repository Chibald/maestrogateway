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

class MaestroCommandValue:
    def __init__(self, maestrocommand, commandvalue):
        self.command = maestrocommand
        self.value = commandvalue

commands = []
# Daemon Control Messages
commands.append(MaestroCommand('Refresh', 0, 'Refresh'))
commands.append(MaestroCommand('GetInfo', 0, 'GetInfo'))
# Maestro Control Messages
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
commands.append(MaestroCommand('Fan_State', 37, 'int'))# 0, 1, 2, 3 ,4,  5 ,6
commands.append(MaestroCommand('Control_Mode', 40, 'onoff')) # 0 = Auto , 1 = Manual
# Untested, proceed with caution
commands.append(MaestroCommand('Feeding_Screw', 34, '49')) # write 49 as parameter to socket foor feeding screw activiation
commands.append(MaestroCommand('Celsius_Fahrenheit', 49, 'int'))
commands.append(MaestroCommand('Sleep', 57, 'int'))
commands.append(MaestroCommand('Summer_Mode', 58, 'onoff'))
commands.append(MaestroCommand('Pellet_Sensor', 148, 'onoff'))
commands.append(MaestroCommand('Adaptive_Mode', 149, 'onoff'))
commands.append(MaestroCommand('AntiFreeze', 154, 'int'))
commands.append(MaestroCommand('Reset_Active', 2, '255'))
commands.append(MaestroCommand('Reset_Alarm', 1, '255'))
# Probably bit dangerous ;)
#commands.append(MaestroCommand('Factory_Reset', 46, 'onoff'))

def getMaestroCommand(commandname):
    i = 0
    while i < len(commands):
        if commandname == commands[i].name:
            return commands[i]    
        i += 1
    return MaestroCommand('Unknown', -1, 'Unknown')

def maestroCommandToWriteParametri(maestrocommandval):
    write = ""
    maestrocommand = maestrocommandval.command
    if maestrocommand.name == "GetInfo":
        write = "C|RecuperoInfo"
    else:
        write = "C|WriteParametri|"
        writevalue = float(maestrocommandval.value)
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
    return write