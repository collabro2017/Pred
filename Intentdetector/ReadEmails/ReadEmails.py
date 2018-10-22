import pandas as pd
import pickle

print('reading data...')

data = pd.read_csv('split_emails.csv')

split_emails = data.values.tolist() # 10.000 emails

emails = []

for i in range(0,len(split_emails)):
	# print('\n--------------------------------------------------------------------------------------')
	sections = split_emails[i][2].split('\r\n')
	inMailBody = False
	content = {}
	for j in sections:
		# print(j)
		# if('noreply' in str(j) or 'do not need reply' in str(j) ):
		# 	print('**************************************************************************** \n '
		# 		+ '***************************************************************************')
		# 	print(j)
		if j.strip() == '' and not inMailBody:
			# print('**** MAIL BODY ****')
			inMailBody = True
			content['Message'] = ''
			continue
		if not inMailBody:				
			if (len(j.split(':',1))>1):
				content[j.split(':',1)[0]] = j.split(':',1)[1]
		else:
			content['Message'] = content['Message'] + j
	emails.append(content)


print('Writing pickle file emailsList: where each element of the list is a dictionary of emails.')

with open('pkl/emailsList.pkl','wb') as f:
    pickle.dump( emails, f )

print('file written as pkl/emailsList.pkl')
