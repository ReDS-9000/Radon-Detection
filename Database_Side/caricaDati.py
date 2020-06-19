import json,os,threading,pymysql
from subprocess import PIPE, Popen


def prendiJson(path):
	dati=json.load(open(path,"r"))
	return dati


def scaricaDati():
	

	os.system("python getfile.py")

	global tsd
	tsd=threading.Timer((20), scaricaDati)
	tsd.start()
	return




def esegui(command):
	process = Popen(args=command, stdout=PIPE, shell=True)
	return process.communicate()[0]




def carica(dati):

	db = pymysql.connect("192.168.5.3","Radon","Ioni2020!","Radon" )
	cursor = db.cursor()

	id=dati["id"]
	for i in dati.keys():
		if(i=="id"):
			continue
		timestamp=str(dati[i])
		totalcount=str(dati[i]["totalcount"])
		countMin=str(dati[i]["countMin"])
		comando="INSERT INTO dati (Timestamp,conteggitot,conteggimin,centralina) VALUES (%s,%s,%s,%s);"%(timestamp,totalcount,countMin,id)
		cursor.execute(comando)
		db.commit()
	return






def upload():

	lsFile=str(esegui("ls nuoviDati/"))
	lsFile=lsFile.split("\\")
	lsFile.remove("n")

	for i in lsFile:
		dati=prendiJson("nuoviDati/"+str(i))
		carica(dati)

	global tu
	tu=threading.Timer((20), scaricaDati)
	tu.start()







scaricaDati()
upload()




















