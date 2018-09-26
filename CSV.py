import csv
import FeatureExtractor as fe

FILE = "Output.csv"


def listtocsv(inboxEmailFeatures,Output,result_1,result_2,result_3):
	header = ["sender_frequency","Cc","is_interrogative_text","is_automated_mail","Actual Status","Random Forrest","Decision Tree","Support Vector Machine"]
	inboxSize = len(inboxEmailFeatures)
	with open(FILE,'w') as csvfile:
		writer=csv.writer(csvfile,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(header)
		for i in range(0,inboxSize):
			row = inboxEmailFeatures[i]
			row.append(Output[i])
			row.append(result_1[i])
			row.append(result_2[i])
			row.append(result_3[i])
			writer.writerow(row)
