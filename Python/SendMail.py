#coding: utf-8
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import time
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

	def Create(self):					#
		self.msg = MIMEMultipart()			#
		# FORMT #					#
		self.msg['From'] = self.fromaddr		#	INDIRIZZO MITTENTE (deve coincidere con il login)
		self.msg['To'] = self.toaddr			#	INDIRIZZO DESTINATARIO
		self.msg['Subject'] = self.subj			#	OGGETTO
		body = self.body				#	CORPO
		# FORMT #					#
		self.msg.attach(MIMEText(self.body, 'plain'))	#	CREAZIONE MAIL
		return self.msg					#

	def attachThis(self):
		
		path=self.dirpath + self.filename						#	IMPOSTAZIONE DEL PATH AL FILE
		attachment = open(path, "rb")							#	LETTURA FILE
												#
		part = MIMEBase('application', 'octet-stream')					#	PREPARAZIONE ALLA CODIFICA DELL'ALLEGATO
		part.set_payload((attachment).read())						#	PREPARAZIONE ALLA CODIFICA IN BASE64
		encoders.encode_base64(part)							#	CODIFICA IN BASE64
		part.add_header('Content-Disposition', "attachment; filename= %s" % self.filename)	#	CREAZIONE DELL'ALLEGATO
		self.msg.attach(part)								#	INSERIMENTO DELL'ALLEGATO
		print "File attached: " + self.filename						#	RIEPILOGO
		return 0									#
		
	def getPass(self):
		return self.passwd
	
	def getUser(self):
		return self.fromaddr
	
	def getmessage(self):
		return self.msg
	
	def Send(self):
		
		# COMM #
		print "Contacting server..."
		server = smtplib.SMTP('smtp.gmail.com', 587)				#	SELEZIONE SERVER SMTP
		server.starttls()							#	INIZIO COMUNICAZIONE CON SERVER
		print "Logging..."							#	
		server.login(self.fromaddr, self.passwd)				#	PROCEDURA DI LOGIN (indirizzo mail, password)
		text = self.msg.as_string()						#	SELEZIONE MAIL E CONVERSIONE
		print "Sending..."							#
		server.sendmail(self.fromaddr, self.toaddr, text)			#	INVIO MAIL (INDIRIZZO MITTENTE, INDIRIZZO DESTINATARIO,MAIL CONVERTITA)
		server.quit()								#	CHIUSURA COMUNICAZIONI CON SERVER 
		print "Mail sent. Closing communication with smtp server. \n \n DONE"
		
		# COMM #







file_txt="home/pi/radon/registrati_"+str(datetime.now().strftime ("%Y:%m:%d:%H:%M:%S"))

os.rename("/home/pi/radon/rilevazione.txt",file_txt)

Mail=mail(					#	CREAZIONE MAIL (fromaddress, password, toaddress, subject, body, filename, dirpath)
"radon@majoranaorvieto.org",			#	INDIRIZZO MITTENTE
"********",					#	PASSWORD MITTENTE
"os19_radon@majoranaorvieto.org", 	#	INDIRIZZO DESTINATARIO
"RADON - RILEVAZIONE",						#	OGGETTO
						#	CORPO
"Nuova rilevazione",
				#
file_txt,			#	NOME FILE
""				#	PATH FILE
)

Mail.Create()

Mail.attachThis()	#	INSERIMENTO DELL'ALLEGATO (Nome file CON ESTENSIONE,Directory del file CON / ALLA FINE)
Mail.Send()
os.system('rm '+str(file_txt))
