import time
import os,sys,json,threading
from shutil import copyfile
from datetime import datetime
from urllib.request import urlopen

#https://maxpromer.github.io/LCD-Character-Creator/
#PATH file rivelazione /home/pi/radon/
#PATH file backup /home/pi/radon/backup/
#PORTA COM default /dev/ttyACM0  Baudrate 115200

def connection():
	try:
		ser = serial.Serial('/dev/ttyACM0', 115200)		#/dev/tty/ACM0 POTREBBE CAMBIARE
		return ser
	except:
		sys.exit()



def checkInternet():
	global sent
	try:
		response = urlopen('https://www.google.com/', timeout=1.5)
		#scrive sul display "connesso a internet"
		ser.write(1)
		if not sent:
			mandaDati()
			#scrive sul display "dati mandati"
			ser.write(2)
			sent=True
	except:
		sent=False
	global tci
	tci=threading.Timer((10), checkInternet)
	tci.start()
	return


def mandaDati():

	while(1):
		try:
			tsd.cancel()
			break
		except:
			continue

	os.system("python sendMail.py")

	copyfile("/home/pi/radon/nativeJson.json","/home/pi/radon/rilevazione.json")
	scriviDati()
	return


def prendiJson():
	dati=json.load(open("/home/pi/radon/rilevazione.json","r"))
	return dati

def salvaJson(dati):
	with open("/home/pi/radon/rilevazione.json","w") as outfile:
		json.dump(dati,outfile,indent=8)
	return


def calcolaCountMin():
	timenow=time.time()
	minutes=round((timenow-startTime)/60.0)
	if(minutes==0): minutes=1
	countMin=totalCount/minutes
	return countMin
	
def backup():
	copyfile ("/home/pi/radon/rilevazione.json", ("/home/pi/radon/backup/backup_" + str(datetime.now ().strftime ("%Y:%m:%d:%H:%M:%S") ) + ".json"))
	#scrive sul display "backup effettuato"
	ser.write(3)
	with open("/home/pi/radon/backup/backupConteggi.json","w") as outfile:
		json.dump({"conteggi":totalCount},outfile,indent=8)
	return


def scriviDati():
	dati = prendiJson()
	tempoOra=datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
	countMin=calcolaCountMin()

	dati[tempoOra]={}
	dati[tempoOra]["totalCount"]=totalCount
	dati[tempoOra]["countMin"]=countMin

	salvaJson(dati)

	backup()

	global tsd
	tsd = threading.Timer((60*15), scriviDati)
	tsd.start()

	return

def prendiConteggi():
	dati=json.load(open("/home/pi/radon/backup/backupConteggi.json","r"))
	conteggi=dati["conteggi"]
	return conteggi



#t.cancel() da infilare
global totalCount
global startTime


sent=False
totalCount = prendiConteggi()

ser=connection()

if(not os.path.exists("/home/pi/radon/rilevazione.json")):
	copyfile("/home/pi/radon/nativeJson.json","/home/pi/radon/rilevazione.json")

startTime=time.time()



scriviDati()
checkInternet()

while(1):

	received = int(ser.readline())

	if(received==1):
		totalCount+=1

	elif(received==2):
		while(1):
			try:
				tsd.cancel()
				break
			except:
				continue
		while(1):
			try:
				tci.cancel()
				break
			except:
				continue
		with open("/home/pi/radon/backup/backupConteggi.json","w") as outfile:
			json.dump({"conteggi":totalCount},outfile,indent=8)
		#scrive sul display "raspberry spento, staccare la spina"
		ser.write(5)
		os.system("systemctl poweroff")
	elif(received==3):
		while(1):
			try:
				tsd.cancel()
				break
			except:
				continue
		while(1):
			try:
				tci.cancel()
				break
			except:
				continue
		with open("/home/pi/radon/backup/backupConteggi.json","w") as outfile:
			json.dump({"conteggi":0},outfile,indent=8)
		totalCount=0
		startTime=time.time()
		scriviDati()
		checkInternet()
		#scrive sul display "reset effettuato"
		ser.write(4)



