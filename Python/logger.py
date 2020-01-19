#############################################################
#                                                           #                                                                     
#	VOCABOLARIO                                               #                                                                  
#                                                           #
#	PartialC = somma tic che verra azzerata ogni 15m          #
#                                                           #                                                                    
#	TIC = segnale in arrivo dal contatore                     #                                                                                                                                                                                                                                         
#                                                           #                                                                     
#	NextTime = ora attuale + 15m                              #
#	                                                          #
#	Time = ora attuale                                        #                                                                                                                                                                                                                 
#                                                           #                                                                                                                                                
#############################################################

######################################################
#IMPORT                                              #
                                                     #
import time, httplib                                 #
																									   #
import os,sys																				 #
																										 #
import serial, commands                              #
                                                     #
from shutil import copyfile                          #

import json											 #
                                                     #
from datetime import datetime, timedelta						 #
                                                     #
######################################################

#######################################################################################
def Connection():                                                                     #
	try:                                                                                #
		ser = serial.Serial('/dev/ttyACM0', 115200)		#/dev/tty/ACM0 POTREBBE CAMBIARE    #                                              #
		return ser                                                                        #
	except:                                                                             #                                                      #
		sys.exit()                                                                        #
 
                                                                                      #
def CheckInternet():                                                                  #
	conn = httplib.HTTPConnection("www.google.com", timeout=1.5)                        #
	try:                                                                                #
		conn.request("HEAD", "/")                                                         #
		conn.close()                                                                      #
		return True                                                                       #
	except:                                                                             #
		conn.close()                                                                      #
	return False                                                                        #
                                                                                      #
#######################################################################################
ser = Connection()

#tutto sto coso serve pe aggiunge 15m senza srecchia il formato dell'ora#
NextTime=(datetime.now()+timedelta(minutes=15)).strftime("%H:%M:%S")

TIC = 0

os.system("touch /home/pi/radon/rilevazione.txt")

while (True): 
	Time = datetime.now ().strftime ("%H:%M:%S") 
	if (NextTime <= Time): 
		#qui crea il file finale, all'inizio lo chiamo solo rilevazione cosi la la aggiungiamo all'ultimo prima di inviarla cosi non sbricchia la data# 
		FinalRilevation = open ("/home/pi/radon/rilevazione.txt", "a") 
		FinalRilevation.write (str(datetime.now ().strftime ("%Y:%m:%d:%H:%M:%S") )+";" + str(TIC) + "\n")
		FinalRilevation.close () 

		copyfile ("/home/pi/radon/rilevazione.txt", ("/home/pi/radon/backup/backup_" + str(datetime.now ().strftime ("%Y:%m:%d:%H:%M:%S") ) + ".txt")) 
		TIC = 0

		NextTime=(datetime.now()+timedelta(minutes=15)).strftime("%H:%M:%S")
	received = int(ser.readline()) 
	if received == 1:
		
		TIC = TIC + 1
	elif received == 2:
		if CheckInternet() == True:
			Date = datetime.datetime.now().strftime ("%d_%m_%Y")
			os.rename ("/home/pi/radon/rilevazione.txt", ("/home/pi/radon/rilevazione" + "_" + str(Date) + ".txt"))
			os.system("python SendMail.py")
