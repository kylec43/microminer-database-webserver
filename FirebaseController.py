import firebase_admin
from firebase_admin import credentials, firestore
import Constants

class FirebaseController:
	cred = credentials.Certificate('ServerAccountKey.json')
	default_app = firebase_admin.initialize_app(cred)

	def __init__(self):
		pass

	def upload(self, originalUrlKeywords, kwicUrlKeywords, noiseWords):
		

		db = firestore.client()
		doc_ref = db.collection(Constants.COLLECTION_SAMPLE).document(Constants.DOCUMENT_QUERY_URLS)
		doc_ref.set({
			Constants.ARG_NOISE_WORDS: noiseWords,
			Constants.ARG_URL_ORIGINAL_KEYWORDS: originalUrlKeywords,
			Constants.ARG_KWIC_KEYWORD_DATA: kwicUrlKeywords
		})


	def getQueryResults(self, keywords):
		db = firestore.client()
		doc_ref = db.collection(Constants.COLLECTION_SAMPLE).document(Constants.DOCUMENT_QUERY_URLS)
		doc = doc_ref.get().to_dict()

		urlsKeywords = doc[Constants.ARG_KWIC_KEYWORD_DATA]
		originalUrlKeywords = doc[Constants.ARG_URL_ORIGINAL_KEYWORDS]
		noiseWords = doc[Constants.ARG_NOISE_WORDS]
		keywords = [keyword for keyword in keywords if not keyword in noiseWords]
		print('keywords:', keywords)
		queryResults = ''
		foundUrls = []

		if len(keywords) != 0:
			for data in urlsKeywords:

				if not data[Constants.ARG_URL] in foundUrls:

					dataKeywords = [x.lower() for x in data[Constants.ARG_KEYWORDS].split()]


					if all(x in dataKeywords for x in keywords):

						for x in originalUrlKeywords:

							if x[Constants.ARG_URL].lower() == data[Constants.ARG_URL].lower():
								foundUrls.append(x[Constants.ARG_URL])
								queryResults += (x[Constants.ARG_URL] + ' ' + x[Constants.ARG_KEYWORDS] + '\n')
								break

		print('results:', queryResults)
		return queryResults