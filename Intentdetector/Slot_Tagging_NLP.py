# This scripts loads a pretrained model and a input file in CoNLL format (each line a token, sentences separated by an empty line).
# The input sentences are passed to the model for tagging. Prints the tokens and the tags in a CoNLL format to stdout
# Usage: python RunModel_ConLL_Format.py modelPath inputPathToConllFile
from __future__ import print_function
from preprocessing import readCoNLL, createMatrices, addCharInformation, addCasingInformation
import keras
import sys
import logging
import os

# gets only the name of the file without the file type (e.g: from data/input.txt to input)
def getFileNameFromPath(inputPath):
    with open(inputPath,'r') as file:
        return '.'.join((os.path.basename(file.name)).split(".")[:-1])


if len(sys.argv) < 3:
    print("Usage: python RunModel_CoNLL_Format.py modelPath inputPathToConllFile")
    exit()

modelPath = sys.argv[1]
inputPath = sys.argv[2]
inputColumns = {0: "tokens"}


# :: Prepare the input ::
sentences = readCoNLL(inputPath, inputColumns)
addCharInformation(sentences)
addCasingInformation(sentences)


# :: Load the model ::
lstmModel = BiLSTM.loadModel(modelPath)


dataMatrix = createMatrices(sentences, lstmModel.mappings, True)

# :: Tag the input ::
tags = lstmModel.tagSentences(dataMatrix)

# This will be used to name our results directory and results file: 
onlyFileName = getFileNameFromPath(inputPath)
onlyModelName = getFileNameFromPath(modelPath)

# :: Output to stdout ::
#Directory where the results will be stored. If dir doesnt exist a dir MyResults/modelName will be created for you.
resultsDir = 'MyResults/'+onlyModelName
if not os.path.isdir(resultsDir):
    os.makedirs(resultsDir)
results = open(resultsDir +'/conll-results-'+onlyFileName+'.txt','w') #Saving the results as conll-results-name.txt

for sentenceIdx in range(len(sentences)):
    tokens = sentences[sentenceIdx]['tokens']
    for tokenIdx in range(len(tokens)):
        tokenTags = []
        for modelName in sorted(tags.keys()):
            tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])
        results.write("%s\t%s" % (tokens[tokenIdx], "\t".join(tokenTags)) + "\n") 
        print("%s\t%s" % (tokens[tokenIdx], "\t".join(tokenTags)))
    results.write("\n")  
    print("")

results.close() 