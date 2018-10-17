import email
from bs4 import BeautifulSoup
import EmailFetcher as ef
import Classifier as cf
from pprint import pprint
import CSV

userEmail = 'example@gmail.com'
DEFAULT = "default-id"

interrogative_words=["could", "which", "what" , "whose" , "who", "whom" ,"where", "when" ,"how" ,"why", "wherefore" ,"whether","question","need answer"]
negative_words=["unsubscribe","no-reply","noreply","mailer","automated"]


def words_present(all_text,keyword_list):   #checks if any word in all_text is present in keyword_list
    if all_text == None :
        return False
    if any(word in all_text for word in keyword_list) :
        return True
    return False


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
    message = email.message_from_string(emailString)
    
    mail={}
    mail["From"]=email.utils.parseaddr(message['From'])[1]
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
        emailText = BeautifulSoup(emailText, 'html.parser').get_text()
        
    mail["emailText"]=emailText

    return mail


def read_from_disk(directory):
    emails = []
    for i in range(1,ef.Num_MAIL):
        #print ("\n\n----------------------------------------- Processing mail no:%d --------------------\n"%(i))
        try:
            f = open('%s/%s.eml' %(directory, i), 'r')
            data=f.read()
            emails.append(data)
            f.close()
        except:
            return emails 
    return emails


def senderFrequency(sender,emails):
    cnt=0
    for email in emails:
        if email["From"] == sender:
            cnt=cnt+1
    return cnt
    

def replied(messageid,sentEmails):
        for email in sentEmails:
                if messageid == email["In-Reply-To"]:
                    return 1
        return 0


def dictList(dictionary):
    ret = []
    for i in dictionary.keys():
        ret.append(dictionary[i])
    return ret

def extractFeatures():
    emails = read_from_disk(ef.INBOX_DIRECTORY)
    
    inboxEmails = []
    sentEmails = []

    #seprate sent and inbox emails
    for email in emails:
        email = parseEmail(email)
        if email["From"] == userEmail:
            sentEmails.append(email)
        else :
            inboxEmails.append(email)
                               
    inboxEmailFeatures = []
    output = []
    
    # find numerical features
    for email in inboxEmails :
        features = {}
        features["sender_frequency"] = senderFrequency(email["From"],inboxEmails)
        features["is_automated_mail"] = words_present(email["emailText"],negative_words)
        features["is_interrogative_text"] = words_present(email["emailText"] + email["Subject"],interrogative_words)
        features["Cc"]=email["Cc"]
        #features["reply"] = replied(email["Message-ID"],sentEmails)
        featureslist = dictList(features)
        output.append(replied(email["Message-ID"],sentEmails))
        inboxEmailFeatures.append(featureslist)

    #Machine Learning

    print ("Applying Machine Learning...\n")
    inboxSize = len(inboxEmailFeatures)
    halfSize = int(inboxSize/2)

    result_1,result_2,result_3 = cf.classifiers(inboxEmailFeatures[:halfSize],output[:halfSize],inboxEmailFeatures[halfSize:])

    # dumping in csv
    CSV.listtocsv(inboxEmailFeatures[:halfSize],output[:halfSize],result_1,result_2,result_3)
        
        

        