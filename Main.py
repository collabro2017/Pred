import FeatureExtractor as fe
import EmailFetcher as ef

def main(username, password) :
        print ("\nFetching Emails...\n")
        ef.login(username, password)
        print ("Extracting Features...\n")
        fe.extractFeatures()
