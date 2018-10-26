from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

from helpers import parse_into_emails
from query import EmailDataset

emails = pd.read_csv('split_emails.csv') 
email_df = pd.DataFrame(parse_into_emails(emails.message))
email_df.drop(email_df.query("body == '' | to == '' | from_ == ''").index, inplace=True)

stopwords = ENGLISH_STOP_WORDS.union(['ect', 'hou', 'com', 'recipient'])
vec = TfidfVectorizer(analyzer='word', stop_words=stopwords, max_df=0.3, min_df=2)
vec_train = vec.fit_transform(email_df.body)

# print out the vector of the first email
print(vec_train[0:1])

# Find cosine similarity between the first email and all others.
cosine_sim = linear_kernel(vec_train[0:1], vec_train).flatten()
# print out the cosine similarities
# print(cosine_sim)

# Finding emails related to a query.
queries = ['invoice','Package','Delivery']

# Transform the query into the original vector
for query in queries:
	print('\n=================================================================')
	vec_query = vec.transform([query])

	cosine_sim = linear_kernel(vec_query, vec_train).flatten()

	# Find top 10 most related emails to the query.
	related_email_indices = cosine_sim.argsort()[:-10:-1]
	# print out the indices of the 10 most related emails.
	print(related_email_indices)

	for i in related_email_indices:
		print('--------------------------------------------------------------------------')
		print(email_df.body.values[i])

# Use the EmailDataset class to query for keywords.

for query in queries:
	print('==============================================')
	ds = EmailDataset()
	results = ds.query(query, 10)

	# Print out the first result.
	print(ds.find_email_by_index(results[0]))
