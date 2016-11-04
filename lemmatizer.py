'''
    File name: lemmatizer.py
    Author: Gangeshwar Krishnamurthy
    Email: gangeshwark@gmail.com
    Date created: 11/04/2016
    Python Version: 2.7
    Description: Contains a class MyLemmatizer used to lemmatize words. Removes verb inflictions and plurals.
'''

from nltk.stem import WordNetLemmatizer


class MyLemmatizer():

	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()

	def lemmatize(self, word, postag='v'):
		"""
		Lemmatize function to lemmatize a word. Removes verb inflictions and plurals also.
		Args:
			word: word to lemmatize.
			postag: if the word is a verb, noun or adj. Defaults to verb ('v')
				Pass v to the variable to remove verb inflictions.
		"""
		if isinstance(word, str):
			return self.lemmatizer.lemmatize(word, pos=postag)
		else:
			try:
				return self.lemmatizer.lemmatize(str(word), pos=postag)
			except Exception, e:
				return "TypeError: Cannot convert input type to string."


#Testing code
if __name__ == '__main__':
	ml = MyLemmatizer()
	print ml.lemmatize("abandonment")
	print ml.lemmatize("chairs")
	print ml.lemmatize("absorbing")
	
	print ml.lemmatize("sad")
	print ml.lemmatize("angry")
	print ml.lemmatize("scared")
	print ml.lemmatize("disgusting")	

	print ml.lemmatize("joyful")
	print ml.lemmatize("surprising")
	print ml.lemmatize("admirable")
	print ml.lemmatize("interesting")