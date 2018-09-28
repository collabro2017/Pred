import imaplib
import smtplib
import os
import email as em
from bs4 import BeautifulSoup
from random import randint
import sys

from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid

from subprocess import call
from textwrap import dedent

import csv
import pickle


import Main
import datetime

import time



def isImportantEmail(email):
    print("Checking if the email is worth replying")

    Main.main(username, password)
    isAutomated = []
    isInterrogative = []
    shouldReply = []

    with open("Output.csv","r") as f:
        csvReader = csv.reader(f, delimiter = ",",quotechar="|")
        for row in (csvReader):
                if "" in row:
                    continue
                if not len(row)==0:
                    isInterrogative.append(row[2])
                    isAutomated.append(row[3])
                    shouldReply.append(row[4]) 

    # Removing headers
    shouldReply = shouldReply[1:] 
    isAutomated = isAutomated[1:]
    isInterrogative = isInterrogative[1:]

    if shouldReply[0] == "1" or (isAutomated[0] == "0" and isInterrogative[0].upper() == "TRUE"):
        print("Should reply to this email\n\n")
        return True

    print("\n\n")
    return False



def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def generate_ids(n):
    ids = []
    for i in range(0,n):
        diff_id = False
        id_n = random_with_N_digits(6) 
        while id_n in ids:
            id_n = random_with_N_digits(6)
        ids.append(id_n)

    return ids

def extract_text( email_message_instance):
    message = ""
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                message = message + part.get_payload()
    elif maintype == 'text':
        message = message + email_message_instance.get_payload()
    return message

def parseEmail(emailString):
    message = em.message_from_string(emailString)
    
    mail={}
    mail["From"]=em.utils.parseaddr(message['From'])[1]
    mail["Subject"]=message['Subject']
    mail["Message-ID"]=message["Message-ID"]

    if "Cc" in message.keys():
        mail["Cc"] =  1
    else:
        mail["Cc"] =  0

    if "In-Reply-To" in message.keys():
        mail["In-Reply-To"] =  message["In-Reply-To"]
    else:
        mail["In-Reply-To"] =  DEFAULT

    emailText = extract_text(message)

    if emailText != None:
        emailText = BeautifulSoup(emailText, features="html.parser").get_text()
    mail["emailText"]=emailText

    return mail

def combineEmailsDic(firstDic, secondDic):
    resultingDic = {}
    for i in range(0, len(secondDic)):
        resultingDic[i] = secondDic[i]
    
    counter = len(secondDic)
    for i in range(0, len(firstDic)-len(secondDic)):
        resultingDic[counter] = firstDic[i]
        counter += 1

    return resultingDic

def getInboxEmails(username, password, Num_MAIL=10):

    status,mailboxes = imap.list()

    MAILBOX = "Inbox"

    status,data = imap.select(MAILBOX)

    emails = []

    if(status == "OK"):
        status,data = imap.search(None,"ALL")
        emailIds = data[0].split()
        usefulVars['inboxLen'] = len(emailIds)

        if(len(emailIds)<Num_MAIL):
            Num_MAIL = len(emailIds)

        for i in range(-1,-(Num_MAIL+1),-1 ):
                rv,mail = imap.fetch(emailIds[i], "(RFC822)")
                if rv != 'OK' :
                    print ("ERROR getting message", -i)
                    continue
                emails.append(mail[0][1].decode("utf-8"))


        inboxEmails = []
        sentEmails = []

        for email in emails:
            email = parseEmail(email)
            if email["From"] == "example@mail.com":
                sentEmails.append(email)
            else :
                inboxEmails.append(email)
    else :
        print ("Unable to access ",MAILBOX)
        imap.logout()
        # exit()

    return inboxEmails


def create_auto_reply(original):
    mail = MIMEMultipart('alternative')
    mail['Message-ID'] = make_msgid()
    mail['References'] = mail['In-Reply-To'] = original['Message-ID']
    mail['Subject'] = 'Re: ' + original['Subject']
    mail['From'] = username
    mail['To'] = original['Reply-To'] or original['From']
    mail.attach(MIMEText(dedent(body % usefulVars['randId']), 'plain'))
    return mail

def send_auto_reply(original):
    smtp.sendmail(
       username, [original['From']],
        create_auto_reply(original).as_bytes())
    log = 'Replied to “%s” for the mail “%s”' % (original['From'],
                                                 original['Subject'])
    print(log)
    try:
        call(['notify-send', log])
    except FileNotFoundError:
        pass

def reply(mail_number):
    imap.select(readonly=True)
    _, data = imap.fetch(mail_number, '(RFC822)')
    imap.close()
    send_auto_reply(message_from_bytes(data[0][1]))
    imap.select(readonly=False)
    imap.store(mail_number, '+FLAGS', '\\Answered')
    imap.close()

def tagEmailThreads(username, password):
    inboxEmails = getInboxEmails(username,password)
    randomIDs = generate_ids(len(inboxEmails))

    myDic = {}

    for i in range(0, len(inboxEmails)):
        myDic[i] = {"email":inboxEmails[i], "id": randomIDs[i]} 

    print("writing emailsDict pkl file in pkl/emailsDict.pkl")
    with open('pkl/emailsDict.pkl','wb') as f:
        pickle.dump(myDic, f)

    print("done")

def checkNewMail(username, password):
    inboxEmails = getInboxEmails(username,password)

    with open('pkl/emailsDict.pkl','rb') as f:
        emailsDict = pickle.load(f)

    newEmails = []
    randomIDs = []

    newEmailsInInbox = False
    newEmailsCounter = 0

    anImportantMail = False

    for i in range(0, len(inboxEmails)):
        if(inboxEmails[i]["Message-ID"] != emailsDict[0]['email']['Message-ID']):
            print("There are new emails in the inbox")
            newEmailsInInbox = True
            newEmails.append(inboxEmails[i])
            if(isImportantEmail(inboxEmails[i])):
                anImportantMail = True
                rand = random_with_N_digits(6)
                usefulVars['randId'] = rand
                reply(str(usefulVars['inboxLen']-i))
                randomIDs.append(rand)
            else:
                print("New email not worth replying to.")
        else:
            break

    if((newEmailsInInbox)):
        newEmailsDic = {}
        for i in range(0, len(newEmails)):
            if anImportantMail:
                newEmailsDic[i] = {"email":newEmails[i], "id": randomIDs[i]} 
            else:
                newEmailsDic[i] = {"email":newEmails[i]}

        newEmailsDic = combineEmailsDic(emailsDict, newEmailsDic)

        print("writing emailsDict pkl file in pkl/emailsDict.pkl")
        with open('pkl/emailsDict.pkl','wb') as f:
            pickle.dump(newEmailsDic, f)

    else:
        print("No new emails in the inbox")

def getData(option="default"):

    option = option.lower()
    if(option=='help'):
        print("Options: \n\n-'content'\n-'subject'\n-'from'\n-'id'\nNothing for default(everything in python dict)")
        return
    if(option != "content" and option != "subject" and option != "from" and option != "id"):
        option = "default"

    mailsLen = input("Introduce the number of emails you'd like to check (nothing for all): \n")

    with open('pkl/emailsDict.pkl','rb') as f:
        emailsDict = pickle.load(f)

    isNumber = True

    try:
        mailsLen = int(mailsLen)
    except ValueError :
        isNumber= False

    if not isNumber:
        mailsLen = len(emailsDict)
    else:
        if mailsLen>len(emailsDict):
            mailsLen = len(emailsDict)

    if(option == 'default'):
        for i in range(0, mailsLen):
            print("\n")
            print(i, ": ", emailsDict[i])
    elif(option == 'content'):
        for i in range(0, mailsLen):
            print("\n")
            print(i, ": ",emailsDict[i]['email']['emailText'])
    elif(option == "subject"):
        for i in range(0, mailsLen):
            print("\n")
            print(i, ': ', emailsDict[i]['email']['Subject'])
    elif(option == "from"):
        for i in range(0, mailsLen):
            print("\n")
            print(i, ': ',emailsDict[i]['email']['From'])
    elif(option == "id"):
        for i in range(0, mailsLen):
            print("\n")
            print(i, ': ',emailsDict[i]['id'])

def main(username,password):

    if not os.path.exists("pkl"):
        try:
            os.makedirs("pkl", exist_ok=True)
        except Exception as e:
            print("Couldnt create directory pkl")
            print(e)

    if(not os.path.isfile('pkl/emailsDict.pkl')):
        print('Fetching emails from ' + str(username))
        tagEmailThreads(username, password)
    else:
        # print("Checking if there are more emails in " + str(username) + "\n")
        print("Checking for more emails")
        checkNewMail(username, password)










imap = imaplib.IMAP4_SSL('imap.gmail.com',993)
smtp = smtplib.SMTP_SSL('smtp.gmail.com')
DEFAULT = "default-id"
Num_MAIL = 10


print("\n\nStarting program. ")


if(len(sys.argv)>1):
    if (sys.argv[1].lower() == 'getdata'):
        option = input('Introduce part of email you want to print. (Enter for default or help to see options) \n')
        getData(option)
        exit()

username = input("Enter email username : ")
password = input("Enter password : ")

try:
    imap.login(username,password)
except imaplib.IMAP4.error as e:
    print ("IMAP LOGIN FAILED... ")
    print (e)
    exit()

try:
    smtp.login(username,password)
except smtplib.smtp.error as e:
    print ("SMTP LOGIN FAILED... ")
    print (e)
    exit()

usefulVars =  {'inboxLen': 0, 'randId':'NULL'}

body = '''
Hello,

Thanks for contacting us.
Your ticket ID is: %s. 

We'll answer your query as soon as posible.

Have a great Day,
This message was generated automatically by our A.I. agent

'''

while(True):
    print('\n--------------------------------------------------------------------------------')
    print("UTC: ", datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y"),'\n')
    main(username, password)
    time.sleep((60*2)) # Waiting 2 min between email checks


