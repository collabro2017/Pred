import pickle
import sys


def removeEmails(n):
    with open('pkl/emailsDict.pkl','rb') as f:
        edic = pickle.load(f)
    for i in range(0,n):
        print(edic.pop(i))
        edic.pop(i,None)
    counter = n
    for i in range(0,len(edic)):
        edic[i] = edic.pop(counter)
        counter += 1
    with open('pkl/emailsDict.pkl','wb') as f:
        pickle.dump(edic, f)


if len(sys.argv)<2:
	print("Missing number of emails to delete")
	print("Use: python Remove_n_Emails.py number")
	exit()

number = int(sys.argv[1])

removeEmails(number)

