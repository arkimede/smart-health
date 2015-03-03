import obd
#obd.debug.console

#def log(msg):
#	print msg

#obd.debug.handler = log

connection = obd.OBD("/dev/pts/0")

temperature = obd.commands['AMBIANT_AIR_TEMP']
pressure = obd.commands['BAROMETRIC_PRESSURE']

if connection.has_command(temperature):
	response = connection.query(temperature)
	print response.value, response.unit, temperature.name, temperature.desc
else:
	print "temperature not supported"

if connection.has_command(pressure):
	response = connection.query(pressure)
	print response.value, response.unit, pressure.name, pressure.desc
else:
	print "temperature not supported"


#for command in connection.supportedCommands:
#	print str(command)
#	response = connection.query(command)
#	print response.value, response.unit

