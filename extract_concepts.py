'''
    File name: extract_concepts.py
    Author: Gangeshwar Krishnamurthy
    Email: gangeshwark@gmail.com
    Date created: 11/03/2016
    Python Version: 2.7
'''
"""
Possible ways to get new concepts:
1. import from other lexicons
2. Extracting new concepts from blogs, new articles etc by using the concept_parser module in Java.

Since I could not make the concept_parser in Java up and running, I am using the method one to get new concepts.
"""
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import random
from lemmatizer import MyLemmatizer
from semantic_similarity import SemanticSimilarity
import operator

def preprocess(word):
	"""Function to lemmatize a word
		1. Remove plurals
		2. Remove verb inflictions
		3. Remove prepositions
		4. Remove conjunctions
		5. Remove Foriegn Language
	"""
	pass


def get_new_concepts():
	"""Extracts new concepts using SenticWordNet(SWN) and Bing Liu's Opinion lexicon.

	Arguments:

	Returns:
		List of new concepts
	"""
	neg_words, pos_words = [], []
	#Section 1: code to extract from SWN.
	#Call preprocess for every word encountered.
	return neg_words, pos_words


def get_random_moodtags(polarity):
	"""
	Randomly chooses two moodtags from a list of 4 moodtags for every polarity.

	Arguments:
		polarity: takes value +1 or -1. +1 indicates positive polarity and -1 indicates negative polarity.

	Returns:
		list with 2 moodtags.
	"""
	positive_moodtags = ['joyful', 'interesting', 'surprising', 'admirable']
	negative_moodtags = ['sad', 'scared', 'angry', 'disgusting']
	moodtags = []
	if polarity == 1:
		random.seed()
		moodtags = random.sample(positive_moodtags, 2)
	elif polarity == -1:
		random.seed()
		moodtags = random.sample(negative_moodtags, 2)

	return moodtags


# This code returns almost 0 for all the values
def get_relevant_moodtags(word, polarity):
	SS = SemanticSimilarity()
	positive_moodtags = ['joyful', 'interesting', 'surprising', 'admirable']
	negative_moodtags=['sad','scared','angry','disgusting']
	
	if polarity == -1:
		#lemmatized each mood. Scores are 0 for sad and angry.
		sad = SS.word_similarity(word, "sad")
		scared = SS.word_similarity(word, "scar")
		angry = SS.word_similarity(word, "angry")
		disgusting = SS.word_similarity(word, "disgust")
		
		mood_values = {	
				'sad':sad,
				'scared':scared,
				'angry':angry,
				'disgusting':disgusting	}
		#sort in the descending order of scores of the mood
		mood_sorted = sorted(mood_values.items(), key=operator.itemgetter(1))
		mood_sorted = reversed(mood_sorted)
		mood_sorted = list(mood_sorted)

	elif polarity == 1:
		#lemmatized each mood. Scores are 0 for joyful and admirable.
		joyful = SS.word_similarity(word, "joyful") 
		interesting = SS.word_similarity(word, "interest")
		surprising = SS.word_similarity(word, "surprise")
		admirable = SS.word_similarity(word, "admirable")
		
		mood_values = {
				'joyful':joyful,
				'interesting':interesting,
				'surprising':surprising,
				'admirable':admirable	}
		#sort in the descending order of scores of the mood
		mood_sorted = sorted(mood_values.items(), key=operator.itemgetter(1))
		mood_sorted = reversed(mood_sorted)
		mood_sorted = list(mood_sorted)
		
	return mood_sorted


def get_semantics(word):
	"""
	Returns a list of words which are closely related to the given concept. 
	All 5 semantics will have same polarity as the input concept.

	Arguments:
		word: the word to find the semantics for.

	Returns:
		a 5-value list of semantics. 
	"""
	semantics = []
	return semantics


def main():
	neg_words, pos_words = get_new_concepts()
	neg_words = ["concerns", "negatives"]
	pos_words = ["achievements", "revelation"]
	for word in neg_words:
		print word
		print get_relevant_moodtags(word, -1)[:2]
		
	for word in pos_words:
		print word
		print get_relevant_moodtags(word, 1)[:2]


if __name__ == '__main__':
	main()