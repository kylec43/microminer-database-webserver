import firebase_admin
from firebase_admin import credentials, firestore
import Constants

class FirebaseController:
	cred = credentials.Certificate('ServerAccountKey.json')
	default_app = firebase_admin.initialize_app(cred)

	def __init__(self):
		pass

	def upload(self, originalUrlKeywords, kwicUrlKeywords):
		

		db = firestore.client()
		doc_ref = db.collection(Constants.COLLECTION_SAMPLE).document(Constants.DOCUMENT_QUERY_URLS)
		doc_ref.set({
			Constants.ARG_URL_ORIGINAL_KEYWORDS: originalUrlKeywords,
			Constants.ARG_KWIC_KEYWORD_DATA: kwicUrlKeywords
		})


	def getUrlsKeywords(self, keywords):
		pass