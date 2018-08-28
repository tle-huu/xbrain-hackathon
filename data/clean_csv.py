import csv
import requests
import xml.etree.ElementTree as ET
import sys

import snowballstemmer
import nltk
from nltk.corpus import stopwords

import re

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

def prepocess(data):
	punctuation = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '__eos__', '\\']
	data = data.lower()
	for punc in punctuation:
		data = data.replace(punc, '')
	# Step 2: tokenize
	data = nltk.word_tokenize(data)
	# Step 3: strip stopwords
	stop = set(stopwords.words('english'))
	# add any additional stopwords we want to use here
	data = [i for i in data if i not in stop]
	stemmer = snowballstemmer.stemmer('english')
	data = stemmer.stemWords(data)

	return data

def main():
	newsitems = parseXML('./hax/data/train.xml')

	savetoCSV(newsitems, 'answers.csv')


if __name__ == "__main__":
	main()
