## Learning-Based-Email-Reply-Prediction

Based on: Intelligent Email Prediction System (IEPS) (Paper in repo)
Developed by Codetrip.es 
Jose Sanchez and Juan Verhook


### Requirements:

python 3.6

Use: 

	pip install -r requirements.txt
	$ python getEmails.py

'''It will prompt you to enter your mail credentials: '''
	Enter gmail username: 
	Enter gmail password: 

	'''Might need to turn off less secure apps for gmail: https://support.google.com/accounts/answer/6010255?hl=en 
	or sign in using App passwords: https://support.google.com/accounts/answer/185833 (recommended) '''

### Email Reading Agent:

Read the last 10 emails from the user inbox and checks for new emails every 2 minutes, if there is a new email the agent will detect if the email requires a respnse or not. 

#### Optional arg 'getdata'

Use:

	$ python getEmails.py getdata

Returns the data stored in pkl/emailsDict.pkl
It will prompt you for an option and the number of emails you want to print :
Options:
-'content'
-'subject'
-'from'
-'id'
-'help': Displays all the options
- None for default(everything in python dict)





