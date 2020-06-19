
import imaplib, email, os, json


contatore=json.load(open("contatore.json","r"))

detach_dir = ''

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login('mail', 'passwd')

m.select("inbox")

resp, items = m.search(None, "(UNSEEN)")
items = items[0].split()

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)")
    print(data)
    email_body = data[0][1]
    mail = email.message_from_string(email_body)
    temp = m.store(emailid, '+FLAGS', '\\Seen')
    m.expunge()

    if mail.get_content_maintype() != 'multipart':
        continue


    if mail["From"] == 'mail':
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            att_path = detach_dir + str(filename)

            if not os.path.isfile(att_path) :
                fp = open("/nuoviDati/nuovoDato"+str(contatore["contatore"])+".json", 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                contatore["contatore"]+=1
                with open("contatore.json","w") as outfile:
                    json.dump(contatore,outfile,indent=8)
