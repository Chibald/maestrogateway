#coding: utf-8

'''
Mapping table

Row 0 corresponds to the position of the information in the MAESTRO frame
Rank 1 corresponds to the title published on the broker
Row 2 (optional) allows you to replace the frame code with corresponding text information

'''
RecuperoInfo=[
	[1,"Stove_State"],
	[2,"Fan_State"],
	[5,"Fume_Temperature"],
	[6,"Ambient_Temperature"],
	[8,"Boiler_Temperature"],
	[10,"Candle_Condition"],
	[11,"ACTIVE_Set"],
	[12,"RPM_Fam_Fume"],
	[13,"RPM_WormWheel_Set"],
	[14,"RPM_WormWheel_Live"],	
	[20,"Active_Mode"],  #0: Désactivé, 1: Activé
	[21,"Active_Live"],
	[22,"Regulation_Mode"],
	[23,"ECO_Mode"],	
	[24,"Silent_Mode"],
	[25,"Chrono_Mode"],
	[26,"Temperature_Setpoint"],
	[27,"Boiler_Setpoint"],
	[28,"Temperature_Motherboard"],
	[29,"Active_Power"],
	[32, "Date_Time_Hours"], # time (0-23)
	[33, "Date_Time_Minutes"], #  (0-29)
	[34, "Date_Day_Of_Month"], # (1-31)
	[35, "Date_Month"], #   (1-12)
	[36, "Date_Year"], # Year of the stove
	[37, "Total_Operating_Hours"],
	[38, "Hours_Of_Operation_In_Power1"], #  (s)
	[39, "Hours_Of_Operation_In_Power2"],
	[40, "Hours_Of_Operation_In_Power3"],
	[41, "Hours_Of_Operation_In_Power4"],
	[42, "Hours_Of_Operation_In_Power5"],
	[43, "Hours_Before_Maintenance"],
	[44, "Minutes_Before_Extinction"],
	[45, "Number_Of_Ignitions"],
	[49, "Sound_Effects_State"],
	[51, "Mode"],
]