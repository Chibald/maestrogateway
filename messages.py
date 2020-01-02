# coding: utf-8
from enum import Enum 

'''

'''

class MaestoMessage(Enum):
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

RecuperoInfo = [ 
    [1, "Stove_State"],
    [2, "Fan_State"],
    [5, "Fume_Temperature"],
    [6, "Ambient_Temperature"],
    [8, "Boiler_Temperature"],
    [10, "Candle_Condition"],
    [11, "ACTIVE_Set"],
    [12, "RPM_Fam_Fume"],
    [13, "RPM_WormWheel_Set"],
    [14, "RPM_WormWheel_Live"],
    [20, "Active_Mode"],  # 0: Désactivé, 1: Activé
    [21, "Active_Live"],
    [22, "Control_Mode"],
    [23, "ECO_Mode"],
    [24, "Silent_Mode"],
    [25, "Chrono_Mode"],
    [26, "Temperature_Setpoint"],
    [27, "Boiler_Setpoint"],
    [28, "Temperature_Motherboard"],
    [29, "Power_Level"],
    [32, "Date_Time_Hours"],  # time (0-23)
    [33, "Date_Time_Minutes"],  # (0-29)
    [34, "Date_Day_Of_Month"],  # (1-31)
    [35, "Date_Month"],  # (1-12)
    [36, "Date_Year"],  # Year of the stove
    [37, "Total_Operating_Hours"],
    [38, "Hours_Of_Operation_In_Power1"],  # (s)
    [39, "Hours_Of_Operation_In_Power2"],
    [40, "Hours_Of_Operation_In_Power3"],
    [41, "Hours_Of_Operation_In_Power4"],
    [42, "Hours_Of_Operation_In_Power5"],
    [43, "Hours_To_Service"],
    [44, "Minutes_To_Switch_Off"],
    [45, "Number_Of_Ignitions"],
    [49, "Sound_Effects_State"],
    [51, "Mode"],
    # untested
    [3, "DuctedFan1"],
    [4, "DuctedFan2"],    
    [7, "Hydro_1"],  # != 255 == Hydro version
    [9, "ValueBoiler"],  # != 255 == Hydro version
    [15, "3WayValve"],  # 1== Sani, else Risc
    [17, "Brazier"],
    [18, "Profile"],  # 0, 10 = Manual, 1 & 11 = Dynamic, Overnight, Comfort, Power    
    [30, "DatabaseVersion"],
    [30, "FirmwareVersion"],
    [46, "Active_Temperature"],
    [47, "Celcius_Or_Fahrenheit"],
    [48, "Sound_Effects"],
    [50, "Sleep"],
    [52, "WifiSondeTemperature1"],
    [53, "WifiSondeTemperature2"],
    [54, "WifiSondeTemperature3"],
    [56, "SetPuffer"],
    [57, "SetBoiler"],
    [58, "Hydro_3"],  # != 255 == Hydro version
    [59, "ReturnValue"],            
    [60, "AntiFreeze"]
]
