#coding: utf-8
import serial
import time
import sys
import alarm
import datetime as dt

def Connection():
	try:											
		ser = serial.Serial('/dev/ttyACM0', 115200)	
		print "Port found and connected"			#Connessione alla porta seriale
		return ser
	except:											
		print "Error. Check port"	
		return -1

def Send(ser,cmd):
	print("Got command: " + str(cmd) + "  Now writing")		
	line = ser.write(cmd)					#Scrittura comando
	print str(cmd) + " Sent to serial"						
	
	print "\n"

	print "Waiting reply"									
	response=int(ser.readline())			#Attesa conferma
	print "Got reply: " + str(response)	
	if response==121:
		return 0
	elif response==1:
		return 1
	else:
		return -1

def Listening(ser):
	bip=int(ser.readline())
	return bip

def getStringTime():
	ts = time.time()
	st = dt.datetime.fromtimestamp(ts).strftime('%d\%m\%Y-%H:%M:%S')
	return st

def saveFile(fileToSave,N_file):
	
	#Salva il file passato
	fileToSave.close()
	#Prende l'ora corrente
	fileName = 'File'+str(N_file)+'.txt'
	#Genera il nuovo file con la data come nome
	newFile = open(str(fileName), "w")
	currentTimeString = getStringTime()
	newFile.write("Detection starts at: " + currentTimeString+ "\n")
	
	return newFile

def calculateDelta(startTimeInS, finishTimeInS):
	
	deltaInSeconds = finishTimeInS - startTimeInS
	
	return deltaInSeconds
def Numero_ricevuto(numero):
	if numero==33:
		os.system('reboot')
	if numero==107:
		ser.write('121')


def main():
	ser=Connection()

	if ser==-1:
		#Led rimangono spenti
		sys.exit()
	else:
		#Accendere led di stato
		#Controlla se arduino funziona
		Check=Send(ser,str(107))
		time.sleep(1.5)
	if Check==-1:
		sys.exit('Arduino does not respond')
	Accendi=Send(ser,'2')
	if Accendi==-1:
		sys.exit('Arduino does not respond')
	N_file=1
	currentLog = open('File'+str(N_file)+'.txt', "w")#crea il primo file come File1.txt I seguenti saranno File2.txt File3.txt e cos' via
	currentTimeString = getStringTime()
	currentLog.write("Detection starts at: " + currentTimeString+ "\n")
	startTimeInS=time.time()
	bip_tot=0
	startTimeWrite=time.time()
	
    #Se siamo arrivati qui, arduino funziona e anche il geiger. Può iniziare l'ascolto dei segnali
	while 1:
		finishTimeWrite=time.time()
		if calculateDelta(startTimeWrite,finishTimeWrite)>=900:
			currentLog.write(getStringTime()+','+str(bip_tot))      #fa il timestamp dell'ultimo  quarto d'ora''
			startTimeWrite=time.time()
			bip_tot=0
		finishTimeInS=time.time()
		if calculateDelta(startTimeInS,finishTimeInS)>=3600:
			N_file+=1	#cosi il prossimo file si chiamera con il numero successivo
			currentLog=saveFile(currentLog,N_file)
			startTimeInS=time.time()

		Check=Send(ser,str(107))
		if Check==-1:
			sys.exit('Arduino does not responde')
		#Se in 5 minuti non arriva nessun segnale, interrompi l'ascolto e fai un check
		maxWaitingTime = 300 #seconds
		bip = 0
		try:
			with alarm.Timeout(id_='a', seconds=maxWaitingTime):
				bip = Listening(ser)
		except alarm.TimeoutError as e: #No impulses for 5 minutes
			print 'raised', e.id_
			
			Check=Send(ser,"107")                        #controlla se arduino funge
			if Check==-1:
				saveFile(currentLog,N_file)
				sys.exit('Arduino does not responde')

		  #Incrementa la variabile dei bip
		if bip == 1:
			bip_tot=bip_tot+1
		else:
			Numero_ricevuto(bip)


if __name__=="__main__":
	sys.exit(main())
