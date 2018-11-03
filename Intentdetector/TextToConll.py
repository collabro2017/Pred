"""
Converts a text file to CoNLL format and stores it as filename.conll in the same directory as the txt file
"""
import nltk
from neuralnets.BiLSTM import BiLSTM
import re
import sys

if len(sys.argv) < 2:
    print("Missing argument")
    print("Usage: python TextToConll.py input.txt")
    print("input.txt: Path to txt file that will be converted to CoNLL format.")
    exit()

inputPath = sys.argv[1]

def sentencesToConll(sentences, filename):
    with open(filename + ".conll","w") as conllFile:
        for i in sentences:
            for j in (i["tokens"]):
                conllFile.write(j + "\n")
            conllFile.write(" " + "\n")

# Using regex to match locations where preceding character is a dot or a comma and the next character isn't a space.
def getCorrectedText(text):
    return re.sub(r'(?<=[.,])(?=[^\s])', r' ', text)

# :: Read input ::
filename = ""
with open(inputPath, 'r') as f:
    text = f.read()
    filename = (f.name).split(".",1)[0] # gets the path and name of the file without the file type (e.g: from path/input.txt to path/input)

# :: Prepare the input ::
text = getCorrectedText(text)
sentences = [{'tokens': nltk.word_tokenize(sent)} for sent in nltk.sent_tokenize(text)]

print("Converting the text file to CoNLL format and storing it as " + filename + ".conll")
sentencesToConll(sentences, filename)