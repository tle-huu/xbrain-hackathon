import pickle

# Load the stackoverflow dictionnary of words-vectors
file_Name = "en_model"
fileObject = open(file_Name,'rb')
en_model = pickle.load(fileObject)
fileObject.close()

# Turn a sentence to a vector
def sentence2vec(sentence):
	try:
		sentence = str(sentence)
	except Exception as e:
		return None
	if sentence == None:
		return None
	split = sentence.split(" ")
	length = len(split)
	vector = [0] * 300
	for word in split:
		if word in en_model.vocab:
			for i in range(300):
				vector[i] += en_model[word][i]
		else:
			length -= 1
	if not length:
		return None
	for i in range(300):
		vector[i] /= length
	return (vector)
