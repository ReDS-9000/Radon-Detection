import json,os,threading,pymysql


def prendiJson(path):
	dati=json.load(open(path,"r"))
	return dati


def scaricaDati():

	os.system("python getfile.py")

	global tsd
	tsd=threading.Timer((20), scaricaDati)
	tsd.start()
	return







def carica(dati):

	db = pymysql.connect("ip","user","pasword","db" )
	cursor = db.cursor()

	id=dati["id"]
	for i in dati.keys():
		if(i=="id"):
			continue
		timestamp=i
		totalcount=str(dati[i]["totalCount"])
		countMin=str(dati[i]["countMin"])
		comando="INSERT INTO dati (Timestamp,conteggitot,conteggimin,centralina) VALUES ('%s',%s,%s,'%s');"%(timestamp,totalcount,countMin,id)
		print(comando)
		cursor.execute(comando)
		db.commit()
	return






def upload():
	lsFile=os.listdir("nuoviDati/")
	print(lsFile)
	if(len(lsFile)!=0):
		for i in lsFile:
			dati=prendiJson("nuoviDati/"+str(i))
			carica(dati)
			os.system("rm nuoviDati/"+str(i))

	global tu
	tu=threading.Timer((20), upload)
	tu.start()







scaricaDati()
upload()




















