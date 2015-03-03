import obd
import time
import random
#obd.debug.console

#def log(msg):
#	print msg

#obd.debug.handler = log

old_temperature = 0
old_pressure = 0

#connection = obd.OBD("/dev/pts/1")

#temperature = obd.commands['AMBIANT_AIR_TEMP']
#pressure = obd.commands['BAROMETRIC_PRESSURE']



temp_file_log = open("obd_temperatore.log", "a+")

pres_file_log = open("obd_pressure.log", "a+")

while 1:
	temperature = random.randint(-300,300)
	pressure = random.randint(0,300)
	
	if old_temperature != temperature:
		temp_file = open("obd_temperature", "w")
		temp_file.write(str(temperature))
		temp_file.close()
		old_temperature = temperature
	else:
		print "temperature is not changed!\n"
	
	if old_pressure != pressure:
		pres_file = open("obd_pressure", "w")
		pres_file.write(str(pressure))
		pres_file.close()
		old_pressure = pressure
	else:
		print "pressure is not changed!\n"

	pres_file_log.write(str(pressure) + "\n")
	pres_file_log.flush()
	print("pres:"+ str(pressure)+ "\n")
	print("old_pres:"+ str(old_pressure)+"\n")
	temp_file_log.write(str(temperature) + "\n")
	temp_file_log.flush()
	print("temp:"+ str(temperature)+ "\n")
	print("old_temp:"+ str(old_temperature)+"\n")
	                                                                
	time.sleep(30)


#for command in connection.supportedCommands:
#	print str(command)
#	response = connection.query(command)
#	print response.value, response.unit

