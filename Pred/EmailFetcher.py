import imaplib
import FeatureExtractor as fe
import os

INBOX_DIRECTORY="email/inbox"   #Path where Inbox emails are saved
Num_MAIL=200  #Number of mails to save on disk

MAILBOX = "[Gmail]/All Mail"
# MAILBOX = "INBOX"


def saveToFolder(num,data,directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            print("Couldnt save to folder, make sure email/inbox directory exists")

    f = open('%s/%s.eml' %(directory, -num), 'wb')
    f.write(data)
    f.close()


def saveEmails(imap):
    Num_MAIL=200  #Number of mails to save on disk
    MAILBOX = "inbox"

    print('MAILBOX = ', MAILBOX)

    status,data = imap.select(MAILBOX)
    
    if status == 'OK' :
        status,data = imap.search(None,"ALL")
        emailIds = data[0].split()

        if(len(emailIds)<Num_MAIL):
            Num_MAIL = len(emailIds)

        for i in range(-1,-Num_MAIL,-1):
            rv,mail = imap.fetch(emailIds[i], "(RFC822)")
            if rv != 'OK' :
                print ("ERROR getting message", -i)
                return
            # fe.parseEmail(mail[0][1])
            saveToFolder(i,mail[0][1],INBOX_DIRECTORY)
    else :
        print ("Unable to access ",MAILBOX)
        exit()


def login():
    username = input("Enter emailid : ")
    password = input("Enter password : ")

    imap = imaplib.IMAP4_SSL('imap.gmail.com',993)

    # imap = imaplib.IMAP4_SSL('imap-mail.outlook.com', 993)
    try:
        imap.login(username,password)
    except imaplib.IMAP4.error as e:
        print ("LOGIN FAILED... ")
        print (e)

    status,mailboxes = imap.list()
    #print status,mailboxes
    saveEmails(imap)
    imap.logout()
