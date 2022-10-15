#coding: utf-8
'''
MCZ Maestro Command class
These are the supported commands to be set via websocket
'''

from datetime import datetime

class MaestroCommand(object):
    """Maestro Command. Consists of a readable name., a websocket ID and a command type."""
    def __init__(self, name, id, commandtype, commandcategory):
        self.name = name # Name in Json Command
        self.maestroid = id # Maestro command ID to be sent via websocket
        self.commandtype = commandtype # Command type
        self.commandcategory = commandcategory # Command type

class MaestroCommandValue(object):
    """Keyvaluepair: Maestrocammand and value"""
    def __init__(self, maestrocommand, commandvalue):
        self.command = maestrocommand
        self.value = commandvalue

MAESTRO_COMMANDS = []
# Daemon Control Messages
MAESTRO_COMMANDS.append(MaestroCommand('Refresh', 0, 'Refresh', 'Daemon'))
MAESTRO_COMMANDS.append(MaestroCommand('GetInfo', 0, 'GetInfo', 'GetInfo'))
MAESTRO_COMMANDS.append(MaestroCommand('Temperature_Setpoint', 42, 'temperature', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Boiler_Setpoint', 51, 'temperature', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat', 1111, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat_T1', 1108, 'temperature', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat_T2', 1109, 'temperature', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Chronostat_T3', 1110, 'temperature', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Power_Level', 36, 'int', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Silent_Mode', 45, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Active_Mode', 35, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Eco_Mode', 41, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Sound_Effects', 50, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Power', 34, 'onoff40', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Fan_State', 37, 'int', 'Basic'))# 0, 1, 2, 3 ,4,  5 ,6
MAESTRO_COMMANDS.append(MaestroCommand('DuctedFan1', 38, 'int', 'Basic'))# 0, 1, 2, 3 ,4,  5 ,6
MAESTRO_COMMANDS.append(MaestroCommand('DuctedFan2', 39, 'int', 'Basic'))# 0, 1, 2, 3 ,4,  5 ,6
MAESTRO_COMMANDS.append(MaestroCommand('Control_Mode', 40, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Profile', 149, 'int', 'Basic'))
# Untested, proceed with caution
MAESTRO_COMMANDS.append(MaestroCommand('Feeding_Screw', 34, '49', 'Basic')) # 49 as parameter to socket for feeding screw activiation
MAESTRO_COMMANDS.append(MaestroCommand('Celsius_Fahrenheit', 49, 'int', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Sleep', 57, 'int', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Summer_Mode', 58, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Pellet_Sensor', 148, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Adaptive_Mode', 149, 'onoff', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('AntiFreeze', 154, 'int', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Reset_Active', 2, '255', 'Basic'))
MAESTRO_COMMANDS.append(MaestroCommand('Reset_Alarm', 1, '255', 'Basic'))
# Probably bit dangerous ;)
#commands.append(MaestroCommand('Factory_Reset', 46, 'onoff', 'Basic'))

# Diagnostics commands
MAESTRO_COMMANDS.append(MaestroCommand('Diagnostics', 100, 'onoff', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('RPM_Fam_Fume', 1, 'int', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('RPM_WormWheel', 2, 'int', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('Active', 3, 'int', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('Ignitor', 4, 'onoff', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('FrontFan', 5, 'percentage', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('DuctedFan1', 6, 'percentage', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('DuctedFan2', 7, 'percentage', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('Pump_PWM', 8, 'percentage', 'Diagnostics'))
MAESTRO_COMMANDS.append(MaestroCommand('3wayvalve', 9, 'onoff', 'Diagnostics'))

# Datetime commands
MAESTRO_COMMANDS.append(MaestroCommand('Set_DateTime', 0, 'datetime', 'SetDateTime')) # The value to the command has to be given as string in the format - > "ddmmYYYYHHmm", e.g. "171220201636" for the date 17/12/2020 04:36 pm.

def get_maestro_command(commandname):
    """Return Maestro command from the command list by name"""
    i = 0
    while i < len(MAESTRO_COMMANDS):
        if commandname == MAESTRO_COMMANDS[i].name:
            return MAESTRO_COMMANDS[i]
        i += 1
    return MaestroCommand('Unknown', -1, 'Unknown', 'Unknown')

def maestrocommandvalue_to_websocket_string(maestrocommandval):
    """Return string to write on the websocket by Maestro command and Value"""
    write = ""
    maestrocommand = maestrocommandval.command
    if maestrocommand.commandcategory == "GetInfo":
        write = "C|RecuperoInfo"      
    elif maestrocommand.commandcategory == "SetDateTime":
        try:
            if (maestrocommandval.value == "NOW"):
                now = datetime.now()
                write = "C|SalvaDataOra|" + str(now.strftime("%d%m%Y%H%M"))
            else:    
                # Check if value is a valid date else exception is thrown
                datetime.strptime(maestrocommandval.value, "%d%m%Y%H%M")
                write = "C|SalvaDataOra|" + str(maestrocommandval.value)
        except:
            pass     
    else:
        if maestrocommand.commandcategory == "Diagnostics":
            write = "C|Diagnostica|"
        else:
            write = "C|WriteParametri|"
        
        if maestrocommandval.value == "ON":
            maestrocommandval.value = 1
        elif maestrocommandval.value == "OFF":
            maestrocommandval.value = 0

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
        elif maestrocommand.commandtype == "percentage":
            writevalue = int(writevalue)
            if writevalue > 100:
                writevalue = 100
            elif writevalue < 0:
                writevalue = 0                            
        write += str(maestrocommand.maestroid) + "|" + str(writevalue)
    return write
