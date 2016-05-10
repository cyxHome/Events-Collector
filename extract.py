def parseCategory(line):
	# print line
	for i in range(len(tags_list)):
		if tags_list[i] == line.strip():
			return i
	print line
	return None

def readTextAndLabel(category_label, event_text):
	# read the training data into event_text and category_label
	f = open('text', 'r')
	status = 0
	buffered_text = ""
	for line in f:
		if status == 0:
			if line == "\n":
				continue
			label = parseCategory(line)
			category_label.append(label)
			status += 1
		# five continuous newline, means new event would be the next. 
		elif line == "\n" and status >= 5:
			status = 0
			event_text.append(buffered_text)
			buffered_text = ""
		# one newline
		elif line == "\n":
			status += 1
		# a line with text
		else:
			buffered_text += line
			status = 1


def extractKeywords(category_label, event_text):
	from topia.termextract import extract
	keywords_count = {}
	# training data, use first 150 entries in the dataset. 
	for i in range(202):
		extractor = extract.TermExtractor()
		a = extractor(event_text[i])
		for pair in a:
			if pair[0] in keywords_count:
				keywords_count[pair[0]] += pair[1]
			else:
				keywords_count[pair[0]] = pair[1]
	import operator
	sorted_keywords_count = sorted(keywords_count.items(), key=operator.itemgetter(1))
	tmp = []
	import re
	for sorted_keyword_count in sorted_keywords_count:
		if re.match('^[A-Za-z ]*$', sorted_keyword_count[0]) is not None:
			tmp.append(sorted_keyword_count)
	sorted_keywords_count = tmp
	total_extracted_keywords_count = len(sorted_keywords_count)
	# choose the most frequent 500 keywords as features
	keywords = sorted_keywords_count
	f2 = open('keywords', 'w')
	for keyword in keywords:
		f2.write(keyword[0] + "\n")
		

def readKeywords(keywords):
	f = open('keywords', 'r')
	for line in f:
		keywords.append(line.strip())

def buildX(event_text, keywords):
	import pandas as pd
	from topia.termextract import extract
	X = []
	for i in range(len(event_text)):
		text = event_text[i]
		x = {}
		for keyword in keywords:
			x[keyword] = 0
		extractor = extract.TermExtractor()
		pairs = extractor(event_text[i])
		for pair in pairs:
			if pair[0] in keywords:
				x[pair[0]] += pair[1]
		X.append(x)
	return pd.DataFrame(X)

def sample(percentage, data):
	return data.sample(frac=percentage)

training_data = data.sample(frac=0.8)
testing_data = data.sample(frac=0.2)


def classify(model, X):
	return model.predict(X)


for i in range(len(X_testing.loc[1])):
	if X_testing.loc[1][i] > 0:
		print X_testing.columns[i]



# print event_text

# from topia.termextract import tag
# tagger = tag.Tagger()
# tagger.initialize()
# tokenized_text = tagger.tokenize(input_text)
# print tokenized_text

