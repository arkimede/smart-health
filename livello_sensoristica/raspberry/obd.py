import obd
import time
#obd.debug.console

#def log(msg):
#	print msg

#obd.debug.handler = log

old_temperature = 0
old_pressure = 0

connection = obd.OBD("/dev/pts/0")

temperature = obd.commands['AMBIANT_AIR_TEMP']
pressure = obd.commands['BAROMETRIC_PRESSURE']



temp_file_log = open("obd_temperatore.log", "a+")

pres_file_log = open("obd_pressure.log", "a+")

while 1:
	if connection.has_command(temperature):
		response = connection.query(temperature)
		print response.value, response.unit, temperature.name, temperature.desc
		#if old_temperature != response.value:
		temp_file = open("obd_temperature", "w")
		temp_file.write(str(response.value))
		temp_file.close()
		#old_temperature = response.value
		temp_file_log.write(str(response.value) + "\n")
		temp_file_log.flush()
	else:
		print "temperature not supported"
	
	if connection.has_command(pressure):
		response = connection.query(pressure)
		print response.value, response.unit, pressure.name, pressure.desc
		#if old_pressure != response.value:
		pres_file = open("obd_pressure", "w")
		pres_file.write(str(response.value))
		pres_file.close()
		#old_pressure = response.value
		pres_file_log.write(str(response.value) + "\n")
		pres_file_log.flush()
	else:
		print "temperature not supported"

	time.sleep(30)


#for command in connection.supportedCommands:
#	print str(command)
#	response = connection.query(command)
#	print response.value, response.unit

