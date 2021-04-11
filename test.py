import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('ServerAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'sampleData').document(u'queryURLs')
doc_ref.set({
	u'keywordData': [{u'url': 'http://test.com', u'keywords' : 'this is a test',}]
})