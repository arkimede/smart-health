#!/usr/bin/env python

import web
import sys
import json

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

urls = (
    '/taxi/Taxi1', 'get_taxi_obs',
    '/observations', 'get_observation'	
)

class Row_obs:
    def __init__(self, date, value):
        self.date = date
        self.value = value

class Row:
    def __init__(self, date, temperature, pressure, pm10):
	self.date = date
	self.temperature = temperature
	self.pressure = pressure
	self.pm10 = pm10	

class get_taxi_obs:
    def GET(self):
    	#return "Hello, world!"
	try:
		transport = TSocket.TSocket('130.206.80.46', 10000)
		transport = TTransport.TBufferedTransport(transport)
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		result = ""

		client = ThriftHive.Client(protocol)
		transport.open()
		client.execute("select * "
		    + "from gioakbombaci_taxi1")
	
		table = []
		date = ""
		temperature = ""
		pressure = ""
		pm10 = ""
		cont = 0
		while (1):
			row = client.fetchOne()

			if (row == ""):
			 break
		
			r_o_w = row.split()
			if(r_o_w[0]):
				print r_o_w[0]
				date = r_o_w[0]
			if(r_o_w[1]):
				print r_o_w[1]
				temperature = r_o_w[1]
			if(r_o_w[2]):
				print r_o_w[2]
				pressure = r_o_w[2]
			if(r_o_w[3]):
				print r_o_w[3]
				pm10 = r_o_w[3]

			currentRow = Row(date, temperature, pressure, pm10)
			provaJ = json.dumps(currentRow.__dict__)
			print provaJ
			print currentRow.temperature		
			table.append(provaJ)
			cont = cont + 1
			# whatever you want to do with this row, here
			result = result + row + "\n"


		#print client.fetchAll()
		transport.close()
		provaJtable = json.dumps(table)
		return provaJtable
	except Thrift.TException, tx:
		return tx.message

class get_observation:
	def GET(self):
		try:
		        transport = TSocket.TSocket('130.206.80.46', 10000)
               		transport = TTransport.TBufferedTransport(transport)
                	protocol = TBinaryProtocol.TBinaryProtocol(transport)
                	result = ""

                	client = ThriftHive.Client(protocol)
                	transport.open()

			parameter = web.input()
			ent_id = parameter.id
			ent_type = parameter.type
                	client.execute("select * from gioakbombaci_"+ent_id+"_"+ent_type)

                	table = []
               		date = ""
                	value = ""
			cont = 0
 	                while (1):
             	           	row = client.fetchOne()

                	        if (row == ""):
       	                 		break
	
                        	r_o_w = row.split()
				if(len(r_o_w)!=2):
					continue
                        	if(r_o_w[0]):
                                	print r_o_w[0]
                                	date = r_o_w[0]
                        	if(r_o_w[1]):
                                	print r_o_w[1]
                                	value = r_o_w[1]
				"""
                        	if(r_o_w[2]):
                                	print r_o_w[2]
                                	pressure = r_o_w[2]
                        	if(r_o_w[3]):
                                	print r_o_w[3]
                                	pm10 = r_o_w[3]
				"""

                        	currentRow = Row_obs(date, value)
                        	provaJ = json.dumps(currentRow.__dict__)
                        	print provaJ
                        	print currentRow.value
                        	table.append(provaJ)
                        	cont = cont + 1
                        	# whatever you want to do with this row, here
                        	result = result + row + "\n"

                	#print client.fetchAll()
                	transport.close()
                	provaJtable = json.dumps(table)
                	return provaJtable
        	except Thrift.TException, tx:
                	return tx.message



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
