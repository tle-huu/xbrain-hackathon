#Python code to illustrate parsing of XML files
# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET
import sys

def parseXML(xmlfile):

	# create element tree object
	tree = ET.parse(xmlfile)

	# get root element
	root = tree.getroot()
	# create empty list for news items
	newsitems = []

	# iterate news items
	for item in root.findall('./questions/question'):

		# empty news dictionary
		news = {}
		# iterate child elements of item
			# special checking for namespace object content:media
		news['category'] = item.attrib['category']
		news['id'] = item.attrib['question_id']
		news['title'] = item.attrib['title']
			# append news dictionary to news items list
		newsitems.append(news)

	# return news items list
	return newsitems


def savetoCSV(newsitems, filename):

    # specifying the fields for csv file
    fields = ['category', 'id', 'title']

    # writing to csv file
    with open(filename, 'w') as csvfile:

        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(newsitems)


def main():
	# parse xml file
	newsitems = parseXML('./hax/data/train.xml')

	# store news items in a csv file
	savetoCSV(newsitems, 'terence.csv')


if __name__ == "__main__":

    # calling main function
    main()


#Python code to illustrate parsing of XML files
# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET
import sys


import snowballstemmer
import nltk
from nltk.corpus import stopwords
import xml

import re

from bs4 import BeautifulSoup

def cleanhtml(raw_html):
	cleantext = BeautifulSoup(raw_html, "html.parser").text

	# cleanr = re.compile('<.*?>')
	# cleantext = re.sub(cleanr, '', raw_html)
	# return cleantext

def remove_tags(text):
	return ''.join(xml.etree.ElementTree.fromstring(text).itertext())

def preprocess(data):
	punctuation = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '__eos__', '\\']
	data = data.lower()
	for punc in punctuation:
		data = data.replace(punc, '')
	# Step 2: tokenize
	# data = nltk.word_tokenize(data)
	# Step 3: strip stopwords
	# stemmer = snowballstemmer.stemmer('english')
	# data = stemmer.stemWords(data)

	return data

def parseXML2(xmlfile):

	# create element tree object
	print("Parsing xml...")
	tree = ET.parse(xmlfile)
	print("Finished parsing xml...")

	# get root element
	root = tree.getroot()
	# create empty list for news items
	newsitems = []

	# iterate news items
	for item in root.findall('./answers/answer'):

		# empty news dictionary
		news = {}

		news['id'] = item.attrib['answer_id']
		news['group'] = item.attrib['group']
		news['elected'] = item.attrib['isElectedAnswer']

		data = item.attrib['text']
		data = preprocess(data)
		# data = remove_tags(data)
		news['text'] = data
		newsitems.append(news)

	# return news items list
	return newsitems


def savetoCSV2(newsitems, filename):

	# specifying the fields for csv file
	fields = ['id', 'group', 'elected', 'text']

	# writing to csv file
	with open(filename, 'w') as csvfile:

		# creating a csv dict writer object
		writer = csv.DictWriter(csvfile, fieldnames = fields)

		# writing headers (field names)
		writer.writeheader()

		# writing data rows
		writer.writerows(newsitems)


def main2():
	# parse xml file
	newsitems = parseXML2('./hax/data/train.xml')
	# store news items in a csv file
	savetoCSV2(newsitems, 'answers.csv')


if __name__ == "__main__":
	main()
	main2()
