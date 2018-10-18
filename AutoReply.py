import csv
import pickle
import os
import sys

from textwrap import dedent
from subprocess import call


from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid

sys.path.insert(0, 'Intentdetector')

# import IntDetMain

def writeData(ticketsIDs):

	web_emailsDict_path = 'G:/Work/AI-EdenLLC/server/g0a_mvp_web-demo/pkl/ticketsReplied.pkl'

	with open('pkl/ticketsReplied.pkl','wb') as f:
		pickle.dump(ticketsIDs, f)

	with open(web_emailsDict_path,'wb') as f:
		pickle.dump(ticketsIDs, f)


def appendIDToData(newID):
	
	if(not os.path.isfile('pkl/ticketsReplied.pkl')):
		ticketsDic = {}
		idx = 0

	else:
		with open('pkl/ticketsReplied.pkl','rb') as f:
			ticketsDic = pickle.load(f)	

		idx = len(ticketsDic)

	ticketsDic[idx] = newID

	writeData(ticketsDic)


def replyAutomatically(emailData, ticketID, emailNumber, imap_service, smtp_service, user):
	print("replying automatically to email: ", ticketID)
	# print(emailData)
	global imap
	global smtp
	global username
	imap = imap_service
	smtp = smtp_service
	username = user

	appendIDToData(ticketID)
	reply(emailNumber, ticketID)


def create_auto_reply(original, randId):
    mail = MIMEMultipart('alternative')
    mail['Message-ID'] = make_msgid()
    mail['References'] = mail['In-Reply-To'] = original['Message-ID']
    mail['Subject'] = 'Re: ' + original['Subject']
    mail['From'] = username
    mail['To'] = original['Reply-To'] or original['From']
    mail.attach(MIMEText(dedent(getReplyContent() % randId), 'plain'))
    return mail


def send_auto_reply(original, randId):
    smtp.sendmail(
       username, [original['From']],
        create_auto_reply(original, randId).as_bytes())
    log = 'Replied to “%s” for the mail “%s”' % (original['From'],
                                                 original['Subject'])
    print(log)
    try:
        call(['notify-send', log])
    except FileNotFoundError:
        pass


def reply(mail_number, randId):
    imap.select(readonly=True)
    _, data = imap.fetch(mail_number, '(RFC822)')
    imap.close()
    send_auto_reply(message_from_bytes(data[0][1]), randId)
    imap.select(readonly=False)
    imap.store(mail_number, '+FLAGS', '\\Answered')
    imap.close()
    

def getReplyContent():

	'''
	Detect Intent and create body of email using machine learning.
	'''

	# Using this body template for now.
	body = '''
	Hello,

	Thanks for contacting us.
	Your ticket ID is: %s. 

	We'll answer your query as soon as posible.

	Have a great Day,
	This message was generated automatically by our A.I. agent

	'''

	return body


def detectIntent(emailText):
	IntDetMain.run()

