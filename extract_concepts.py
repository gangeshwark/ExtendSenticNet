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

	Arguments:
		Word to be preprocessed.

	Returns:
		lemmatized word if the word in American English, else return a empty string.																																																																																																																																																												
	"""
	#check if english word
	english_d = enchant.Dict("en_US")
	split_words = word.split('_')
	for x in split_words:
		try:
			if not english_d.check(x):
				return ''
		except Exception as e:
			print "Enchant error({0}): {1}\nWord: {2}, {3}".format(e.errno, e.strerror, x, word)
	
	word = nltk.word_tokenize(word)
	word = nltk.pos_tag(word)
	# No preposition and conjunction. And no foreign words																																																										
	pos_list = [ 'IN', 'CC', 'FW']
	new_word = []
	for w in word:
		if w[1] not in pos_list:
			new_word.append(ml.lemmatize(w[0]))

	return '_'.join(map(str, new_word))
	

'''
Old function moved to file new_concepts.py
'''
def get_new_concepts():
	"""
	Extracts new concepts from the new words file.

	Arguments: None

	Returns:
		List of new concepts
	"""
	new_pos_words, new_neg_words = [], []
	with open(OUTPUT_BASE_PATH + '/new_positive_words.txt') as posi_file:
		for word in posi_file:
			new_pos_words.append(word)

	with open(OUTPUT_BASE_PATH + '/new_negative_words.txt') as neg_file:
		for word in neg_file:
			new_neg_words.append(word)
	
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
	"""
	Chooses two moodtags from a list of 4 moodtags using it's similarity score with the input word

	Arguments:
		polarity: takes value +1 or -1. +1 indicates positive polarity and -1 indicates negative polarity.

	Returns:
		list with 2 moodtags.
	"""
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
		Looking at the SenticNet data, I observed that semantically related words/concepts for a word/concept is from 
		the same set of data available in SenticNet.
		This can also be thought of intuitively when we want to relate words/concepts using graph representation.
	'''
	#seperate positive concepts and negative concepts from the SenticNet data 
	#to ensure we don't relate concepts with different polarity
	if polarity == 1:
		rank = {}
		print "Polarity: 1", word
		for concept in current_pos_concepts:
			rank[concept] = SS.word_similarity(word, concept)

		#sort in the descending order of scores of the similarity
		rank = sorted(rank.items(), key=operator.itemgetter(1))
		rank = reversed(rank)
		rank = list(rank)[:5]
	

	else:
		rank = {}
		print "Polarity: -1", word
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
	#For the below code to run on the complete pos_words, neg_words lists will take a lot of time.
	#Hence for demo purpose using only few words from each of them.
	neg_words = neg_words[:3]
	pos_words = pos_words[:3]
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