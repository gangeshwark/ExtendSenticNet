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
import nltk
import random
import enchant
from lemmatizer import MyLemmatizer
from semantic_similarity import SemanticSimilarity
import operator
from senticnet4_data import senticnet

CURRENT_SENTICNET_DATA_PATH = 'data/current_senticnet_kb'
BING_LIU_DATA_PATH = 'data/bingliu_lexicon'
OUTPUT_BASE_PATH = 'data/new_data'

SS = SemanticSimilarity()
ml = MyLemmatizer()
current_pos_concepts = [key for (key, value) in senticnet.iteritems() if value[6]=='positive']
current_neg_concepts = [key for (key, value) in senticnet.iteritems() if value[6]=='negative']

def preprocess(word):
	"""
	Function to lemmatize a word
		1. Remove plurals
		2. Remove verb inflictions
		3. Remove negation
		4. Remove prepositions
		5. Remove conjunctions
		6. Remove Foriegn Language																																																																																																																																																													
	"""
	#check if english word
	english_d = enchant.Dict("en_US")
	if not english_d.check(word):
		return ''


	word = nltk.word_tokenize(word)
	word = nltk.pos_tag(word)	
	# No preposition and conjunction. And no foreign words																																																										
	pos_list = [ 'IN', 'CC', 'FW']
	new_word = []
	for w in word:
		if w[1] not in pos_list:
			new_word.append(ml.lemmatize(w[0]))

	return '_'join(map(str, new_word))
	


def get_new_concepts():
	"""
		Extracts new concepts using SentiWordNet(SWN) and Bing Liu's Opinion lexicon.
		Also adding few manually picked up concepts.

	Arguments: None

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
	#Section 1: code to extract concepts from SWN.
	#Call preprocess for every word encountered.
	print "Extracting from SWN"
	swn_all_words = swn.all_senti_synsets()
	for word in swn_all_words:
		word_name = word.synset.name().split('.')[0]
		if word.pos_score() > word.neg_score():
			w = preprocess(word_name)
			if w is not '':
				swn_positive_words.append(w)
		else:
			w = preprocess(word_name)
			if w is not '':
				swn_negative_words.append(w)


	#include only if they are not available in knowledge base of senticnet
	print "Checking SenticNet..."
	# Running time O(n^2). Better solution below.
	"""
	for x in xrange(len(swn_positive_words)):
		if swn_positive_words[x] not in current_concepts:
			new_pos_words.append(swn_positive_words[x])

	for x in xrange(len(swn_negative_words)):
		if swn_negative_words[x] not in current_concepts:
			new_neg_words.append(swn_negative_words[x])
	"""
	#Running time O(n*logn)
	print "Positive Words"
	new_pos_words = list(set(swn_positive_words)-set(current_concepts))
	print "Negative Words"
	new_neg_words = list(set(swn_negative_words)-set(current_concepts))
	"""
	print "Sample SWN: Length: ", len(new_pos_words), len(new_neg_words)
	print new_pos_words[:10]
	print new_neg_words[:10]
	"""
	#Section 2: code to extract concepts from Bing Liu's Opinion lexicon.
	print "Extracting from Bing Liu"
	with open(BING_LIU_DATA_PATH + "/positive-words.txt", 'r') as bing_pos_file:
		for line in bing_pos_file:
			w = preprocess(line)
			if w is not '':
				bing_positive_words.append(w)

	with open(BING_LIU_DATA_PATH + "/negative-words.txt", 'r') as bing_neg_file:
		for line in bing_neg_file:
			w = preprocess(line)
			if w is not '':
				bing_negative_words.append(w)
	
	#include only if they are not available in knowledge base of senticnet
	print "Checking SenticNet..."
	# Running time O(n^2). Better solution below.
	"""
	for x in xrange(len(bing_positive_words)):
		if bing_positive_words[x] not in current_concepts:
			new_pos_words.append(bing_positive_words[x])

	for x in xrange(len(bing_negative_words)):
		if bing_negative_words[x] not in current_concepts:
			new_neg_words.append(bing_negative_words[x])
	"""
	#unique concepts
	#Running time O(n*logn)
	print "Positive Words"
	bing_new_pos_words = list(set(bing_positive_words)-set(current_concepts))
	print "Negative Words"
	bing_new_neg_words = list(set(bing_negative_words)-set(current_concepts))
	"""
	print "Sample Bing Liu: Length: ", len(bing_new_pos_words), len(bing_new_neg_words)
	print bing_new_pos_words
	print bing_new_neg_words
	"""
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


# This code returns 0 for few moods.
def get_relevant_moodtags(word, polarity):

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
		
	return mood_sorted[:2]


def get_semantics(word, polarity):
	"""
	Returns a list of words which are closely related to the given concept. 
	All 5 semantics will have same polarity as the input concept.

	Arguments:
		word: the word to find the semantics for.

	Returns:
		a 5-value list of semantics.
	"""

	'''
	Observation:
		Observing the SenticNet data, I found that the semantically related words/concepts for a word/concepts is from 
		the same set of data available in SenticNet.
		This can also be thought of intuitively when we want to relation between words/concepts using graph.
	'''
	#seperate positive concepts and negative concepts from the SenticNet data 
	#to ensure we don't relate concepts with different polarity
	if polarity == 1:
		rank = {}
		print "POL: 1", word
		for concept in current_pos_concepts:
			rank[concept] = SS.word_similarity(word, concept)

		#sort in the descending order of scores of the similarity
		rank = sorted(rank.items(), key=operator.itemgetter(1))
		rank = reversed(rank)
		rank = list(rank)[:5]
	

	else:
		rank = {}
		print "POL: -1", word
		for concept in current_neg_concepts:
			rank[concept] = SS.word_similarity(word, concept)

		#sort in the descending order of scores of the similarity
		rank = sorted(rank.items(), key=operator.itemgetter(1))
		rank = reversed(rank)
		rank = list(rank)[:5]

	print rank

	semantics = ['semantic1', 'semantic2', 'semantic3', 'semantic4', 'semantic5']
	return rank


def main():
	pos_words, neg_words = [],[]
	pos_words, neg_words = get_new_concepts()

	neg_words = neg_words[:2]
	pos_words = pos_words[:2]
	#Every key in the dictionary is a new concept and the value is a 8-value list with the format as below
	#[#mood_tag1, #mood_tag2, polarity, semantic1, semantic2, semantic3, semantic4, semantic5]
	
	senticvector = {}
	for word in pos_words:
		final_moods = []
		final_semantic = []
		concept_moodtags = get_relevant_moodtags(word, 1)
		concept_semantics = get_semantics(word, 1)
		for mood in concept_moodtags:
			final_moods.append("#" + mood[0])

		for semantic in concept_semantics:
			final_semantic.append(semantic[0])

		vector = final_moods + ['positive'] + final_semantic
		senticvector[word] = vector


	for word in neg_words:
		final_moods = []
		final_semantic = []
		concept_moodtags = get_relevant_moodtags(word, -1)
		concept_semantics = get_semantics(word,-1)
		for mood in concept_moodtags:
			final_moods.append("#" + mood[0])

		for semantic in concept_semantics:
			final_semantic.append(semantic[0])

		vector = final_moods + ['negative'] + final_semantic
		senticvector[word] = vector

	#data to write to python file.
	python_data = "senticnet = {}\n"
	for key, value in senticvector.iteritems():
		string = "senticnet['{0}'] = ['{1}', '{2}', '{3}','{4}', '{5}', '{6}', '{7}', '{8}']\n"
		string = string.format(key, value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7])
		python_data += string
	python_data_file = open('senticnet_new_data.py', 'w+')
	python_data_file.write(python_data)



if __name__ == '__main__':
	main()