import os
import json

os.system("apt-get install python3")
os.system("apt-get install python3-pip")
os.system("pip3 install datetime")
os.system("pip install datetime")

os.system("mkdir /home/pi/radon/")
os.system("mkdir /home/pi/radon/backup")

os.system("mv logger.py /home/pi/radon/")
os.system("mv sendMail.py /home/pi/radon/")


print("Creazione nativeJson")
nativeJson=open("/home/pi/radon/nativeJson.json", 'w')
nativeJson.write("{}")
nativeJson.close()

dati = {"id":raw_input("Inserire ID -> ")}
with open("/home/pi/radon/nativeJson.json", 'w') as outfile:
	json.dump(dati, outfile, indent=8)


print("Creazione backupConteggi")
backupConteggi=open("/home/pi/radon/backup/backupConteggi.json", 'w')
backupConteggi.write("{}")
backupConteggi.close()

dati = {"conteggi" : 0}
with open("/home/pi/radon/backup/backupConteggi.json", 'w') as outfile:
	json.dump(dati, outfile, indent=8)

print("Modificando rc.local")
autostartfile=open("/etc/rc.local","r")
dati=autostartfile.readlines()
autostartfile.close()

comando="python3 /home/pi/radon/logger.py &\n"
dati.insert(18,comando)
dati="".join(dati)
autostartfile=open("/etc/rc.local","w")
autostartfile.write(dati)
autostartfile.close()

print("rimuovo la cartella setup")
os.chdir("/home/pi/Desktop")
os.system("rm -rf *")

print("Done")