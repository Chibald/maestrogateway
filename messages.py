# coding: utf-8
from enum import Enum 

'''
Maestro Response Messages
'''

class MaestroMessageType(Enum):
    """Maestro message type. This information is inside the first frame"""
    Parameters = "00"
    Info = "01"
    Database = "02"
    ExtraParameters = "03"
    ChronoDays = "04"
    Alarms = "0A"
    WifiSonde = "0B"
    DatabaseName = "0D"
    SoftwareVersion = "0E"
    Ping = "PING"

class MaestroInformation(object):
    """Maestro Information. Consists of a readable name., a websocket ID and a command type."""
    def __init__(self, frameid, name, messagetype):
        self.frameid = frameid # Position in recuperoinfo-frame
        self.name = name # Maestro command ID to be sent via websocket
        self.messagetype = messagetype # Message type

MAESTRO_INFORMATION = []
MAESTRO_INFORMATION.append(MaestroInformation(0, "Messagetype", 'MaestoMessageType'))
MAESTRO_INFORMATION.append(MaestroInformation(1, "Stove_State", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(2, "Fan_State", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(3, "DuctedFan1", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(4, "DuctedFan2", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(5, "Fume_Temperature", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(6, "Ambient_Temperature", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(7, "Puffer_Temperature", 'temperature'))  # != 255 == Hydro
MAESTRO_INFORMATION.append(MaestroInformation(8, "Boiler_Temperature", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(9, "NTC3_Temperature", 'temperature'))  # != 255 == Hydro
MAESTRO_INFORMATION.append(MaestroInformation(10, "Candle_Condition", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(11, "ACTIVE_Set", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(12, "RPM_Fam_Fume", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(13, "RPM_WormWheel_Set", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(14, "RPM_WormWheel_Live", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(15, "3WayValve", '3way'))  # 1== Sani, else Risc
MAESTRO_INFORMATION.append(MaestroInformation(16, "Pump_PWM", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(17, "Brazier", 'brazier')) # 0 = Ok, !=0 = CLR
MAESTRO_INFORMATION.append(MaestroInformation(18, "Profile", 'int'))  # 0, 10 = Manual, 1 & 11 = Dynamic, Overnight, Comfort, Power   
MAESTRO_INFORMATION.append(MaestroInformation(19, "Modbus_Address", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(20, "Active_Mode", 'int'))  # 0: Désactivé, 1: Activé
MAESTRO_INFORMATION.append(MaestroInformation(21, "Active_Live", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(22, "Control_Mode", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(23, "ECO_Mode", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(24, "Silent_Mode", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(25, "Chrono_Mode", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(26, "Temperature_Setpoint", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(27, "Boiler_Setpoint", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(28, "Temperature_Motherboard", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(29, "Power_Level", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(30, "FirmwareVersion", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(31, "DatabaseID", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(32, "Date_Time_Hours", 'int'))  # time (0-23)
MAESTRO_INFORMATION.append(MaestroInformation(33, "Date_Time_Minutes", 'int'))  # (0-29)
MAESTRO_INFORMATION.append(MaestroInformation(34, "Date_Day_Of_Month", 'int'))  # (1-31)
MAESTRO_INFORMATION.append(MaestroInformation(35, "Date_Month", 'int'))  # (1-12)
MAESTRO_INFORMATION.append(MaestroInformation(36, "Date_Year", 'int'))  # Year of the stove
MAESTRO_INFORMATION.append(MaestroInformation(37, "Total_Operating_Hours", 'timespan'))
MAESTRO_INFORMATION.append(MaestroInformation(38, "Hours_Of_Operation_In_Power1", 'timespan'))  # (s)
MAESTRO_INFORMATION.append(MaestroInformation(39, "Hours_Of_Operation_In_Power2", 'timespan'))
MAESTRO_INFORMATION.append(MaestroInformation(40, "Hours_Of_Operation_In_Power3", 'timespan'))
MAESTRO_INFORMATION.append(MaestroInformation(41, "Hours_Of_Operation_In_Power4", 'timespan'))
MAESTRO_INFORMATION.append(MaestroInformation(42, "Hours_Of_Operation_In_Power5", 'timespan'))
MAESTRO_INFORMATION.append(MaestroInformation(43, "Hours_To_Service", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(44, "Minutes_To_Switch_Off", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(45, "Number_Of_Ignitions", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(46, "Active_Temperature", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(47, "Celcius_Or_Fahrenheit", 'onoff'))
MAESTRO_INFORMATION.append(MaestroInformation(48, "Sound_Effects", 'onoff'))
MAESTRO_INFORMATION.append(MaestroInformation(49, "Sound_Effects_State", 'onoff')) ########### CHECK!!!
MAESTRO_INFORMATION.append(MaestroInformation(50, "Sleep", 'onoff')) #########################
MAESTRO_INFORMATION.append(MaestroInformation(51, "Mode", 'onoff'))  
MAESTRO_INFORMATION.append(MaestroInformation(52, "WifiSondeTemperature1", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(53, "WifiSondeTemperature2", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(54, "WifiSondeTemperature3", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(55, "Unknown", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(56, "SetPuffer", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(57, "SetBoiler", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(58, "SetHealth", 'int'))  # != 255 == Hydro version
MAESTRO_INFORMATION.append(MaestroInformation(59, "Return_Temperature", 'temperature'))
MAESTRO_INFORMATION.append(MaestroInformation(60, "AntiFreeze", 'onoff'))

def get_maestro_info(frameid):
    """Return Maestro info from the commandlist by name"""
    if frameid >= 0 and frameid <= 60:
        return MAESTRO_INFORMATION[frameid]
    else:
        return MaestroInformation(frameid, 'Unknown' + str(frameid), 'int')

def process_infostring(message):
    """convert recuperoinfo message string to array"""
    res = {}
    for i in range(1, len(message.split("|"))):
        info = get_maestro_info(i)
        if info.messagetype == "temperature":
            res[info.name] = float(int(message.split("|")[i], 16))/2
        elif info.messagetype == "timespan":
            res[info.name] = seconds_to_hours_minutes(int(message.split("|")[i], 16))
        elif info.messagetype == "3way":
            if int(message.split("|")[i], 16) == 1:
                res[info.name] = "Sani"
            else:
                res[info.name] = "Risc"
        elif info.messagetype == "brazier":
            if int(message.split("|")[i], 16) == 0:
                res[info.name] = "OK"
            else:
                res[info.name] = "CLR"
        else:
            res[info.name] = int(message.split("|")[i], 16)
    return res

def seconds_to_hours_minutes(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '{:d}:{:02d}:{:02d}'.format(h, m, s)
