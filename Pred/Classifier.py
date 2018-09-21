import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn import svm

def accuracy(output,result):
	match=0	
	length = len(output)
	for i in range(0,length):
		# print(i)
		if output[i]==result[i]:
			match=match+1
	
	return (match/(length+0.0))*100
	
		

def classifiers(trainingFeatures,output,testFeatures):
	trainingFeatures = np.array(trainingFeatures)
	output = np.array(output)
	testFeatures = np.array(testFeatures)
	
	print ("Applying Random Forrest...\n")
	#Random Forrest Classifier
	clf = RandomForestClassifier(n_estimators=50)
	clf = clf.fit(trainingFeatures,output) # ValueError: The number of classes has to be greater than one; got 1(fixed)
	result_1 = clf.predict(testFeatures)
	acc=(accuracy(output,result_1)) # IndexError: index 8 is out of bounds for axis 0 with size 8 (fixed)
	print ("Random Forrest: %.2f "%(acc))

	print ("\nApplying Support Vector Machine...\n")
	#Support Vector Machine
	clf_svm= svm.SVC(C=5)
	clf_svm = clf.fit(trainingFeatures,output) # ValueError: The number of classes has to be greater than one; got 1
	result_2 = clf_svm.predict(testFeatures)
	acc=(accuracy(output,result_2))
	print ("Support Vector Machine: %.2f "%(acc))

	#Decision Tree Classifier
	print ("\nApplying Decision Tree Classifier\n")
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(trainingFeatures,output)
	result_3 = clf.predict(testFeatures)
	acc = (accuracy(output,result_3))
	print ("Decision Tree Classifier: %.2f "%(acc))

	return result_1,result_2,result_3
	
