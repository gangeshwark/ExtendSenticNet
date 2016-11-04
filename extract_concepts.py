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
from senticnet4_data import senticnet

def preprocess(word):
	"""Function to lemmatize a word
		1. Remove plurals
		2. Remove verb inflictions
		3. Remove negation
		4. Remove prepositions
		5. Remove conjunctions
		6. Remove Foriegn Language
	"""
	pass


def get_new_concepts():
	"""Extracts new concepts using SentiWordNet(SWN) and Bing Liu's Opinion lexicon.

	Arguments:

	Returns:
		List of new concepts
	"""
	current_concepts = [key for (key, value) in senticnet.iteritems()]
	print current_concepts[:10]
	bing_negative_words = []
	bing_positive_words = []

	swn_negative_words = []
	swn_positive_words = []
	new_neg_words, new_pos_words = [], []
	#Section 1: code to extract from SWN.
	#Call preprocess for every word encountered.
	print "Extracting from SWN"
	swn_all_words = swn.all_senti_synsets()
	for word in swn_all_words:
		word_name = word.synset.name().split('.')[0]
		if word.pos_score() > word.neg_score():
			swn_positive_words.append(word_name)
		else:
			swn_negative_words.append(word_name)

	

	#include only if they are not available in knowledge base of senticnet
	print "Checking SenticNet..."
	"""
	for x in xrange(len(swn_positive_words)):
		if swn_positive_words[x] not in current_concepts:
			new_pos_words.append(swn_positive_words[x])

	for x in xrange(len(swn_negative_words)):
		if swn_negative_words[x] not in current_concepts:
			new_neg_words.append(swn_negative_words[x])
	"""
	print "Positive Words"
	new_pos_words = list(set(swn_positive_words)-set(current_concepts))
	print "Negative Words"
	new_neg_words = list(set(swn_negative_words)-set(current_concepts))
	print "Sample SWN: Length: ", len(new_pos_words), len(new_neg_words)
	print new_pos_words[:10]
	print new_neg_words[:10]
	
	#Section 2: code to extract concepts from Bing Liu's Opinion lexicon.
	print "Extracting from Bing Liu"
	with open("data/bingliu_lexicon/positive-words.txt", 'r') as bing_pos_file:
		for line in bing_pos_file:
			w = preprocess(line)
			bing_positive_words.append(w)

	with open("data/bingliu_lexicon/negative-words.txt", 'r') as bing_neg_file:
		for line in bing_neg_file:
			w = preprocess(line)
			bing_negative_words.append(w)
	
	#include only if they are not available in knowledge base of senticnet
	print "Checking SenticNet..."
	"""
	for x in xrange(len(bing_positive_words)):
		if bing_positive_words[x] not in current_concepts:
			new_pos_words.append(bing_positive_words[x])

	for x in xrange(len(bing_negative_words)):
		if bing_negative_words[x] not in current_concepts:
			new_neg_words.append(bing_negative_words[x])
	"""
	#unique concepts
	print "Positive Words"
	bing_new_pos_words = list(set(bing_positive_words)-set(current_concepts))
	print "Negative Words"
	bing_new_neg_words = list(set(bing_negative_words)-set(current_concepts))

	print "Sample Bing Liu: Length: ", len(bing_new_pos_words), len(bing_new_neg_words)
	print bing_new_pos_words
	print bing_new_neg_words

	new_pos_words+=bing_new_pos_words
	new_neg_words+=bing_new_neg_words

	return new_pos_words, new_neg_words


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
	pos_words, neg_words = get_new_concepts()
	#print 
	print pos_words[:20]
	print neg_words[:20]
	neg_words = ["concerns", "negatives"]
	pos_words = ["achievements", "revelation"]
	
	for word in pos_words:
		print word
		print get_relevant_moodtags(word, 1)[:2]

	for word in neg_words:
		print word
		print get_relevant_moodtags(word, -1)[:2]


if __name__ == '__main__':
	main()