'''
    File name: lemmatizer.py
    Author: Gangeshwar Krishnamurthy
    Email: gangeshwark@gmail.com
    Date created: 11/04/2016
    Python Version: 2.7
    Description: Contains a class MyLemmatizer used to lemmatize words. Removes verb inflictions and plurals.
'''

from nltk.stem import WordNetLemmatizer
import nltk
import enchant

from nltk.corpus import wordnet
from logger import *

initialize_logger("logs")

class MyLemmatizer():

	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()

	def lemmatize(self, word, postag='v'):
		"""
		Lemmatize function to lemmatize a word. Removes verb inflictions and plurals.
		Args:
			word: word to lemmatize.
			postag: if the word is a verb, noun or adj. Defaults to verb ('v')
				Pass v to the variable to remove verb inflictions.
		"""
		try:
			word = str(word)
			tagged = nltk.pos_tag(nltk.word_tokenize(word))
			return self.lemmatizer.lemmatize(tagged[0][0], pos=get_wordnet_pos(tagged[0][1]))
		except Exception, e:
			return "TypeError: Cannot convert input type to string."


def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.VERB


#Testing code
if __name__ == '__main__':
	ml = MyLemmatizer()
	english_d = enchant.Dict("en_US")
	"""
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

	print ml.lemmatize("anti-american",'n')
	"""

	#Adjectives
	words = ["third", "regrettable", "classiest", "cheapest"]
	print "\nAdjectives ->\tLemmatized"
	for w in words:
		print "{0}\t{1}".format(w, ml.lemmatize(w))

	#Plurals
	words = ["cats", "dogs", "chairs", "brothers", "sisters"]
	print "\nPlurals ->\tLemmatized"
	for w in words:
		print "{0}\t{1}".format(w, ml.lemmatize(w))

	#Verbs
	words = ["assemble", "assess", "assign", "avoid"]
	print "\nVerbs ->\tLemmatized"
	for w in words:
		print "{0}\t{1}".format(w, ml.lemmatize(w))

	#Noun
	words = ["Casino", "wind", "subhumanity", "undergraduates"]
	print "\nNoun ->\tLemmatized"
	for w in words:
		print "{0}\t{1}".format(w, ml.lemmatize(w))

	#Prepositions
	words = ["among", "whether", "around", "until"]
	print "\nPrepositions ->\tLemmatized"
	for w in words:
		print "{0}\t{1}".format(w, ml.lemmatize(w))

	#Conjucations
	words = ["both", "and", "either", "therefore"]
	print "\nConjucations ->\tLemmatized"
	for w in words:
		print "{0}\t{1}".format(w, ml.lemmatize(w))
		"""
		tagged = nltk.pos_tag(nltk.word_tokenize(w))
		print tagged
		print "{0}\t{1}".format(w, ml.lemmatize(tagged[0][0], get_wordnet_pos(tagged[0][1])))
		"""
	for w in words:
		print "Is English? {0}".format(english_d.check(w))

	#Non-american
	#Observed that NTLK POS Tagger didn't identify the individual words in the following list as Non-English words(FW)
	#Hence using enchant lib for the same.
	words = ["gemeinschaft", "salutaris", "quibusdam", "terram"]
	print "\nNon-american ->\tLemmatized"
	for w in words:
		print "{0}\t{1}".format(w, ml.lemmatize(w))

	for w in words:
		print "Is English? {0}".format(english_d.check(w))