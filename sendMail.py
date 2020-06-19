#coding: utf-8
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from datetime import datetime


class mail:
	def __init__(self, fromaddress, password, toaddress, subject, body, filename, dirpath):
		self.fromaddr = fromaddress
		self.passwd = password
		self.toaddr = str(toaddress)
		self.subj = subject
		self.body = str(body)
		self.filename = filename
		self.dirpath = dirpath
		self.msg=None

	def Create(self):
		self.msg = MIMEMultipart()
		# FORMT #
		self.msg['From'] = self.fromaddr				#	INDIRIZZO MITTENTE (deve coincidere con il login)
		self.msg['To'] = self.toaddr					#	INDIRIZZO DESTINATARIO
		self.msg['Subject'] = self.subj					#	OGGETTO
		# FORMT #
		self.msg.attach(MIMEText(self.body, 'plain'))	#	CREAZIONE MAIL
		return self.msg	

	def attachThis(self):
		
		path=self.dirpath + self.filename													#	IMPOSTAZIONE DEL PATH AL FILE
		attachment = open(path, "rb")														#	LETTURA FILE
		part = MIMEBase('application', 'octet-stream')										#	PREPARAZIONE ALLA CODIFICA DELL'ALLEGATO
		part.set_payload((attachment).read())												#	PREPARAZIONE ALLA CODIFICA IN BASE64
		encoders.encode_base64(part)														#	CODIFICA IN BASE64
		part.add_header('Content-Disposition', "attachment; filename= %s" % self.filename)	#	CREAZIONE DELL'ALLEGATO
		self.msg.attach(part)																#	INSERIMENTO DELL'ALLEGATO
		return 0
	
	def Send(self):
		
		# COMM #
		server = smtplib.SMTP('smtp.gmail.com', 587)							#	SELEZIONE SERVER SMTP
		server.starttls()														#	INIZIO COMUNICAZIONE CON SERVER
		server.login(self.fromaddr, self.passwd)								#	PROCEDURA DI LOGIN (indirizzo mail, password)
		text = self.msg.as_string()												#	SELEZIONE MAIL E CONVERSIONE
		server.sendmail(self.fromaddr, self.toaddr, text)						#	INVIO MAIL (INDIRIZZO MITTENTE, INDIRIZZO DESTINATARIO,MAIL CONVERTITA)
		server.quit()															#	CHIUSURA COMUNICAZIONI CON SERVER 
		return True







fileJson="registrati_"+str(datetime.now().strftime ("%Y:%m:%d:%H:%M:%S")+".json")

os.rename("/home/pi/radon/rilevazione.json","/home/pi/radon/"+str(fileJson))

Mail=mail(							#	CREAZIONE MAIL (fromaddress, password, toaddress, subject, body, filename, dirpath)
"mail",			#	INDIRIZZO MITTENTE
"password",						#	PASSWORD MITTENTE
"mail", 		#	INDIRIZZO DESTINATARIO
"Subject",			#	OGGETTO
"Nuovi dati raccolti",				#	CORPO
fileJson,							#	NOME FILE
"/home/pi/radon/"					#	PATH FILE
)

Mail.Create()

Mail.attachThis()	#	INSERIMENTO DELL'ALLEGATO (Nome file CON ESTENSIONE,Directory del file CON / ALLA FINE)
Mail.Send()
os.system('rm '+str(fileJson))
