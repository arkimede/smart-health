#!/usr/bin/python

import time                                	  # Importa libreria per la gestione dei timer
import RPi.GPIO as gpio                           # Importa libreria GPIO
import math

# Inizializzazione GPIO

gpio.setmode(gpio.BCM)                              
gpio.setwarnings(False)                             

gpio.setup(4, gpio.IN, pull_up_down=gpio.PUD_UP)  # GPIO4 input

# Variabili

duration=0					  # singolo intervallo di tempo in cui il segnale d'uscita del sensore resta basso
start_time_measure=0				  # tempo di partenza di una nuova misurazione
sample_time=30					  # tempo di campionamento
start_time=0					  # tempo di partenza di un impulso LOW
stop_time=0					  # tempo di fine di un impulso LOW
low_pulse_occupancy=0				  # quantita' di tempo in cui il segnale e' rimasto basso durante un intervallo di campionamento

# Funzioni
def start_LOW_pulse():
	global start_time			  # attendo il fronte di discesa sul pin GPIO4
	gpio.wait_for_edge(4, gpio.FALLING)
	start_time=time.time()
	#print("GPIO4: Sono LOW!")

def stop_LOW_pulse():
	global stop_time
	gpio.wait_for_edge(4, gpio.RISING)
	stop_time=time.time()			  # attendo il fronte di salita sul pin GPIO4
	#print("GPIO4: Sono HIGH!")

start_time_measure=time.time()
print("Inizio nuova misurazione...")
#out_f=open("shinyei_PM10","w")
out_f_log=open("shinyei_PM10.log", "a+")



# Ciclo infinito
while 1:
	try:
		start_LOW_pulse()
		stop_LOW_pulse()
		duration=stop_time - start_time
		low_pulse_occupancy=low_pulse_occupancy + duration
		if((time.time()-start_time_measure)>sample_time):
			print("Fine misurazione!")
			ratio=(low_pulse_occupancy/sample_time)*100
			concentration=1.1*math.pow(ratio,3)-3.8*math.pow(ratio,2)+520*ratio+0.62
			out_f=open("shinyei_PM10","w")
			out_f.write(str(concentration) + "\n")
			out_f_log.write(str(concentration) + "\n")
			out_f.close()
			print("Dettagli misurazione\n")
			print("LowPulseOccupnacy: ", low_pulse_occupancy)
			print("Ratio: ", ratio)
			print("Concentration: ", concentration)
			low_pulse_occupancy=0
			start_time_measure=time.time()
			print("Inizio nuova misurazione!")
	except KeyboardInterrupt:
		print("Uscita")
		#out_f.close()
		out_f_log.close()
		gpio.cleanup()

