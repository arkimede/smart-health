import os
import io
import time
import sys
import pdb

NUM_ARG=len(sys.argv)
COMMAND=sys.argv[0]

if NUM_ARG==4:
	ENTITY_ID=sys.argv[1]
	ENTITY_TYPE=sys.argv[2]
	POSITION=sys.argv[3]
else:
	print "Usage: " +COMMAND+ " [ENTITY_ID] [ENTITY_TYPE] [POSITION]"
	print
	sys.exit(2) 


OBD_TEMP_PATH = "obd_temperature"
OBD_PRES_PATH = "obd_pressure"
SHINYEI_PM10_PATH = "shinyei_PM10"

lastModifyTemp = 0
lastModifyPres = 0
lastModifyPM10 = 0

#cont = 1

#creo gli id per le tre entita' da ENTITY_ID generale del server
id_temp = "temperature_" + ENTITY_ID
id_pres = "pressure_" + ENTITY_ID
id_pm10 = "pm10_" + ENTITY_ID

#pdb.set_trace()
#fase di creazione delle entita'
create_temp = "python2.7 createEntity.py" + " " + id_temp + " " + ENTITY_TYPE + " " + "position " + "coords "  + POSITION #+ " &" 
os.system(create_temp)
create_temp = "python2.7 createEntity.py" + " " + id_temp + " " + ENTITY_TYPE + " " + "observed_property " + "temperature " + "NaN" #+ " &"
os.system(create_temp)
create_temp = "python2.7 createEntity.py" + " " + id_temp + " " + ENTITY_TYPE + " " + "Service2 " + "text " + "on" #+ " &"
os.system(create_temp)
 
create_press = "python2.7 createEntity.py" + " " + id_pres + " " + ENTITY_TYPE + " " + "position " + "coords "  + POSITION #+ " &" 
os.system(create_press)
create_press = "python2.7 createEntity.py" + " " + id_pres + " " + ENTITY_TYPE + " " + "observed_property " + "pressure " + "NaN" #+ " &"
os.system(create_press)
create_temp = "python2.7 createEntity.py" + " " + id_pres + " " + ENTITY_TYPE + " " + "Service3 " + "text " + "on" #+ " &"
os.system(create_temp)

 
create_pm10 = "python2.7 createEntity.py" + " " + id_pm10 + " " + ENTITY_TYPE + " " + "position " + "coords "  + POSITION #+ " &" 
os.system(create_pm10)
create_pm10 = "python2.7 createEntity.py" + " " + id_pm10 + " " + ENTITY_TYPE + " " + "observed_property " + "PM10 " + "NaN" #+ " &"
os.system(create_pm10)
create_temp = "python2.7 createEntity.py" + " " + id_pm10 + " " + ENTITY_TYPE + " " + "Service1 " + "text " + "on" #+ " &"
os.system(create_temp)

#sottoscrizioni a tutte e tre le entita'

sub_temp = "python2.7 setSubscription.py" + " " + id_temp + " " + "observed_property " + "http://130.206.85.25:7777/accumulate"
sub_press = "python2.7 setSubscription.py" + " " + id_pres + " " + "observed_property " + "http://130.206.85.25:7777/accumulate"
sub_pm10 = "python2.7 setSubscription.py" + " " + id_pm10 + " " + "observed_property " + "http://130.206.85.25:7777/accumulate"

os.system(sub_temp)
os.system(sub_press)
os.system(sub_pm10)

#attendo 45 secondi in modo tale che i file da cui prendere le osservazioni
#abbiamo almeno un valore al loro interno
time.sleep(45)


#coords = ["'38.173079, 15.543566'", "'38.188192, 15.556098'", "'38.206404, 15.557471'"]

while 1:
	#prova = os.path.getmtime("/home/Gioak/Codice-Sensori-Broker/obd_temperature")
	if lastModifyTemp != os.path.getmtime(OBD_TEMP_PATH):
		lastModifyTemp = os.path.getmtime(OBD_TEMP_PATH)
		print "Il file ", OBD_TEMP_PATH, " e' cambiato, invio il nuovo dato"
		temp_file = open(OBD_TEMP_PATH, "r")
		value = temp_file.readline()
		parameters = "python2.7 UpdateEntityAttribute.py" + " " + id_temp + " " + ENTITY_TYPE + " observed_property temperature " + str(value)
		os.system(str(parameters))
	if lastModifyPres != os.path.getmtime(OBD_PRES_PATH):
		lastModifyPres = os.path.getmtime(OBD_PRES_PATH)
		print "Il file ", OBD_PRES_PATH, " e' cambiato, invio il nuovo dato"
		temp_file = open(OBD_PRES_PATH, "r")
		value = temp_file.readline()
		parameters = "python2.7 UpdateEntityAttribute.py"  + " " + id_pres + " " + ENTITY_TYPE + " observed_property pressure " + str(value)
		os.system(str(parameters))
	if lastModifyPM10 != os.path.getmtime(SHINYEI_PM10_PATH):
		lastModifyPM10 = os.path.getmtime(SHINYEI_PM10_PATH)
		print "Il file ", SHINYEI_PM10_PATH, " e' cambiato, invio il nuovo dato"
		temp_file = open(SHINYEI_PM10_PATH, "r")
		value = temp_file.readline()
		parameters = "python2.7 UpdateEntityAttribute.py" + " " + id_pm10 + " " + ENTITY_TYPE + " observed_property PM10 " + str(value)
		os.system(str(parameters))
	#indice = cont % 3
	#value = coords[indice]

	#value = "/"+value+/""
	#parameters = "python2.7 UpdateEntityAttribute.py"  + " " + ENTITY_ID + " " + ENTITY_TYPE + " taxiPosition coords " + str(value)
	#os.system(str(parameters))
	#cont = cont + 1
	time.sleep(30)
