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
    StringData = "AA"
    Ping = "PING"


class MaestroStoveState(object):        
    """Maestro Stove State"""
    def __init__(self, stateid, description, onoroff):
        self.stateid = stateid # Position in recuperoinfo-frame
        self.description = description # Maestro command ID to be sent via websocket
        self.onoroff = onoroff # Message type

class MaestroInformation(object):
    """Maestro Information. Consists of a readable name., a websocket ID and a command type."""
    def __init__(self, frameid, name, messagetype):
        self.frameid = frameid # Position in recuperoinfo-frame
        self.name = name # Maestro command ID to be sent via websocket
        self.messagetype = messagetype # Message type

MAESTRO_STOVESTATE = []
MAESTRO_STOVESTATE.append(MaestroStoveState(0,"Off", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(1,"Checking hot or cold", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(2,"Cleaning cold", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(3,"Loading Pellets Cold", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(4,"Start 1 Cold", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(5,"Start 2 Cold", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(6,"Cleaning Hot", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(7,"Loading Pellets Hot", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(8,"Start 1 Hot", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(9,"Start 2 Hot", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(10,"Stabilising", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(11,"Power 1", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(12,"Power 2", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(13,"Power 3", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(14,"Power 4", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(15,"Power 5", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(30,"Diagnostics", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(31,"On", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(40,"Extinguish", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(41,"Cooling", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(42,"Cleaning Low", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(43,"Cleaning High", 1))
MAESTRO_STOVESTATE.append(MaestroStoveState(44,"UNLOCKING SCREW", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(45,"Auto Eco", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(46,"Standby", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(48,"Diagnostics", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(49,"Loading Auger", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(50,"Error A01 - Ignition failed", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(51,"Error A02 - No flame", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(52,"Error A03 - Tank overheating", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(53,"Error A04 - Flue gas temperature too high", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(54,"Error A05 - Duct obstruction - Wind", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(55,"Error A06 - Bad printing", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(56,"Error A09 - SMOKE PROBE", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(57,"Error A11 - GEAR MOTOR", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(58,"Error A13 - MOTHERBOARD TEMPERATURE", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(59,"Error A14 - DEFECT ACTIVE", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(60,"Error A18 - WATER TEMP ALARM", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(61,"Error A19 - FAULTY WATER PROBE", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(62,"Error A20 - FAILURE OF AUXILIARY PROBE", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(63,"Error A21 - PRESSURE SWITCH ALARM", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(64,"Error A22 - ROOM PROBE FAULT", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(65,"Error A23 - BRAZIL CLOSING FAULT", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(66,"Error A12 - MOTOR REDUCER CONTROLLER FAILURE", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(67,"Error A17 - ENDLESS SCREW JAM", 0))
MAESTRO_STOVESTATE.append(MaestroStoveState(69,"WAITING FOR SECURITY ALARMS", 0))

MAESTRO_INFORMATION = []
MAESTRO_INFORMATION.append(MaestroInformation(0, "Messagetype", 'MaestoMessageType'))
MAESTRO_INFORMATION.append(MaestroInformation(1, "Stove_State", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(2, "Fan_State", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(3, "DuctedFan1", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(4, "DuctedFan2", 'int'))
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
MAESTRO_INFORMATION.append(MaestroInformation(23, "Eco_Mode", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(24, "Silent_Mode", 'int'))
MAESTRO_INFORMATION.append(MaestroInformation(25, "Chronostat", 'int'))
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
MAESTRO_INFORMATION.append(MaestroInformation(47, "Pellet_Sensor", 'int')) # 0 no pellet sensor, 10 pellet sensor w/ enough fuel, 11 pellet sensor w/ no fuel
MAESTRO_INFORMATION.append(MaestroInformation(48, "Celcius_Or_Fahrenheit", 'onoff')) 
MAESTRO_INFORMATION.append(MaestroInformation(49, "Sound_Effects", 'onoff')) 
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
# These items are not really in the information frame but they are transfromed to match commands.
MAESTRO_INFORMATION.append(MaestroInformation(-1, "Power", 'onoff'))
MAESTRO_INFORMATION.append(MaestroInformation(-2, "Diagnostics", 'onoff'))

def get_maestro_info(frameid):
    """Return Maestro info from the commandlist by name"""
    if frameid >= 0 and frameid <= 60:
        return MAESTRO_INFORMATION[frameid]
    else:
        return MaestroInformation(frameid, 'Unknown' + str(frameid), 'int')

def get_maestro_infoname(infoname):
    """Return Maestro command from the message list by name"""
    i = 0
    while i < len(MAESTRO_INFORMATION):
        if infoname == MAESTRO_INFORMATION[i].name:
            return MAESTRO_INFORMATION[i]
        i += 1
    return MaestroInformation(0, 'Unknown', 'int')

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
        
        if info.name == "Stove_State":
            res["Power"] = get_maestro_stoveOnOrOff(res[info.name])
            res["Diagnostics"] = get_maestro_indiagnosticsmode(res[info.name])
        
    return res

def seconds_to_hours_minutes(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '{:d}:{:02d}:{:02d}'.format(h, m, s)

def get_maestro_stoveOnOrOff(stateid):
    i = 0
    while i < len(MAESTRO_STOVESTATE):
        if stateid == MAESTRO_STOVESTATE[i].stateid:
            return MAESTRO_STOVESTATE[i].onoroff
        i += 1
    return 0

def get_maestro_indiagnosticsmode(stateid):
    if stateid == 30 or stateid == 48:
        return 1
    return 0

def get_maestro_stovestatedescription(stateid):
    i = 0
    while i < len(MAESTRO_STOVESTATE):
        if stateid == MAESTRO_STOVESTATE[i].stateid:
            return MAESTRO_INFORMATION[i].description
        i += 1
    return 'unknown'