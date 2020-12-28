#coding: utf-8
'''
MCZ Maestro Command class
These are the supported commands to be set via websocket
'''

class MaestroCommand(object):
    """Maestro Command. Consists of a readable name., a websocket ID and a command type."""
    def __init__(self, name, id, commandtype):
        self.name = name # Name in Json Command
        self.maestroid = id # Maestro command ID to be sent via websocket
        self.commandtype = commandtype # Command type

class MaestroCommandValue(object):
    """Keyvaluepair: Maestrocammand and value"""
    def __init__(self, maestrocommand, commandvalue):
        self.command = maestrocommand
        self.value = commandvalue

MAESTRO_COMMANDS = []
# Daemon Control Messages
MAESTRO_COMMANDS.append(MaestroCommand('Refresh', 0, 'Refresh'))
MAESTRO_COMMANDS.append(MaestroCommand('GetInfo', 0, 'GetInfo'))
# Maestro Control Messages
MAESTRO_COMMANDS.append(MaestroCommand('Temperature_Setpoint', 42, 'temperature'))
MAESTRO_COMMANDS.append(MaestroCommand('Boiler_Setpoint', 51, 'temperature'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat', 1111, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat_T1', 1108, 'temperature'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat_T2', 1109, 'temperature'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat_T3', 1110, 'temperature'))
MAESTRO_COMMANDS.append(MaestroCommand('Power_Level', 36, 'int'))
MAESTRO_COMMANDS.append(MaestroCommand('Silent_Mode', 45, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('Active_Mode', 35, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('Eco_Mode', 41, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('Sound_Effects', 50, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('Power', 34, 'onoff40'))
MAESTRO_COMMANDS.append(MaestroCommand('Fan_State', 37, 'int'))# 0, 1, 2, 3 ,4,  5 ,6
MAESTRO_COMMANDS.append(MaestroCommand('DuctedFan1', 38, 'int'))# 0, 1, 2, 3 ,4,  5 ,6
MAESTRO_COMMANDS.append(MaestroCommand('DuctedFan2', 39, 'int'))# 0, 1, 2, 3 ,4,  5 ,6
MAESTRO_COMMANDS.append(MaestroCommand('Control_Mode', 40, 'onoff')) # 0 = Auto , 1 = Manual
# Untested, proceed with caution
MAESTRO_COMMANDS.append(MaestroCommand('Feeding_Screw', 34, '49')) # 49 as parameter to socket for feeding screw activiation
MAESTRO_COMMANDS.append(MaestroCommand('Celsius_Fahrenheit', 49, 'int'))
MAESTRO_COMMANDS.append(MaestroCommand('Sleep', 57, 'int'))
MAESTRO_COMMANDS.append(MaestroCommand('Summer_Mode', 58, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('Pellet_Sensor', 148, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('Adaptive_Mode', 149, 'onoff'))
MAESTRO_COMMANDS.append(MaestroCommand('AntiFreeze', 154, 'int'))
MAESTRO_COMMANDS.append(MaestroCommand('Reset_Active', 2, '255'))
MAESTRO_COMMANDS.append(MaestroCommand('Reset_Alarm', 1, '255'))
# Probably bit dangerous ;)
#commands.append(MaestroCommand('Factory_Reset', 46, 'onoff'))

def get_maestro_command(commandname):
    """Return Maestro command from the command list by name"""
    i = 0
    while i < len(MAESTRO_COMMANDS):
        if commandname == MAESTRO_COMMANDS[i].name:
            return MAESTRO_COMMANDS[i]
        i += 1
    return MaestroCommand('Unknown', -1, 'Unknown')

def maestrocommandvalue_to_websocket_string(maestrocommandval):
    """Return string to write on the websocket by Maestro command and Value"""
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
