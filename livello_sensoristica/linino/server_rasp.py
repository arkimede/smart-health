import web
import os
#import psutil
import pdb
import sys
#from web.wsgiserver import CherryPyWSGIServer

#CherryPyWSGIServer.ssl_certificate = "./localhost.pem"
#CherryPyWSGIServer.ssl_private_key = "./localhost.key"

urls = (

        '/start/observation', 'start_obs',
        '/stop/observation', 'stop_obs',
	'/quit', 'quit'
)

is_stopped = 0

class quit:
	def GET(self):
		if is_stopped == 1:
			sys.exit(0)
			return "The server is now quitted"
		else:
			return "You can't quit the server, you must send stop observations command before to quit"

# https://localhost/start/observation?id=id_entity&type=&position=
# Questo metodo crea l'entita' observatin su Orion richiamando
# lo script createEntity.py e fa partire lo script per iniziare
# l'osservazione

class start_obs:

        def GET(self):
		#pdb.set_trace()
		tablet_data = web.input()
		id_entity = tablet_data.id
		id_type = tablet_data.type
		position = tablet_data.position
		tokens = position.split()
		position = tokens[0] + '\\ ' + tokens[1]

		#start_obd_sim = "obdsim -g Cycle > obd_sim.out &"
		start_obd = "python2.7 obd.py > obd.out &"
		#start_pm10 = "python2.7 Shinyei.py > shinyei.out &" 
		
		start_send_measures = "python2.7 send_measures.py" + " " + id_entity + " " + id_type + " " + position + " &" 
		#pdb.set_trace()
		#os.system(str(start_pm10))
		#os.system(str(start_obd_sim))
		#inserire una sleep??
		os.system(str(start_obd))
		os.system(str(start_send_measures))

                return "id=" + id_entity + " type=" + id_type + " position=" + position

class stop_obs:

        def GET(self):
		#pdb.set_trace()
		kill_all_proc = "./kill_all.sh"
		os.system(str(kill_all_proc))

		is_stopped = 1
                return "stop observation"


if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()

