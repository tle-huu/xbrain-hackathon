import csv
import requests
import xml.etree.ElementTree as ET
import sys
import nltk
import xml
import re
import string
import enchant
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

TO_PARSE = 'train.xml'
stop_words = set(stopwords.words('english'))

def remove_stopwords(sentence):

	word_tokens = word_tokenize(sentence)

	filtered_sentence = [w for w in word_tokens if not w in stop_words]
	return " ".join(filtered_sentence)



def preprocessQuestions(data):
	punctuation = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '__eos__', '\\']
	numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
	dash = ['-', '_', '+', '&', '/', '*', '=', '$', '#']
	data = data.lower()
	for punc in punctuation:
		data = data.replace(punc, '')
	for number in numbers:
		data = data.replace(number, '')
	for d in dash:
		data = data.replace(d, ' ')
	return remove_stopwords(data)


def preprocessAnswers(data):
	punctuation = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '__eos__', '\\']
	numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

	data = data.lower()
	for punc in punctuation:
		data = data.replace(punc, '')
	for number in numbers:
		data = data.replace(number, '')

	cleanr = re.compile('<pre((.|\n)*?)/pre>|<.*?>')
	cleantext = re.sub(cleanr, '', data)
	d = enchant.Dict("en_US")
	data = ''
	for word in cleantext.split():
		if d.check(word):
			data += word + ' '
	return remove_stopwords(data)


def parseQuestionsXML(xmlfile):
	print("Parsing xml questions...")
	tree = ET.parse(xmlfile)									# create element tree object
	print("Finished parsing xml questions.")
	root = tree.getroot()										# get root element
	newsitems = []												# create empty list for news items
	for item in root.findall('./questions/question'):			# iterate news items
		news = {}												# empty news dictionary
		news['category'] = item.attrib['category']
		news['id'] = item.attrib['question_id']
		data = item.attrib['title']
		data = preprocessQuestions(data)
		news['title'] = data
		newsitems.append(news)									# append news dictionary to news items list
	return newsitems


def parseAnswersXML(xmlfile):
	print("Parsing xml answers...")
	tree = ET.parse(xmlfile)
	print("Finished parsing xml answers.")
	root = tree.getroot()										# get root element
	newsitems = []												# create empty list for news items
	for item in root.findall('./answers/answer'):				# iterate news items
		news = {}
		news['id'] = item.attrib['answer_id']
		news['group'] = item.attrib['group']
		news['elected'] = item.attrib['isElectedAnswer']
		data = item.attrib['text']
		data = preprocessAnswers(data)
		news['text'] = data
		newsitems.append(news)
	return newsitems


def saveQuestionsToCSV(newsitems, filename):
    fields = ['category', 'id', 'title']						# specifying the fields for csv file
    with open(filename, 'w') as csvfile:						# writing to csv file
        writer = csv.DictWriter(csvfile, fieldnames = fields)	# creating a csv dict writer object
        writer.writeheader()									# writing headers (field names)
        writer.writerows(newsitems)								# writing data rows


def saveAnswersToCSV(newsitems, filename):
	fields = ['id', 'group', 'elected', 'text']					# specifying the fields for csv file
	with open(filename, 'w') as csvfile:						# writing to csv file
		writer = csv.DictWriter(csvfile, fieldnames = fields)	# creating a csv dict writer object
		writer.writeheader()									# writing headers (field names)
		writer.writerows(newsitems)								# writing data rows


def main():
	newQuestions = parseQuestionsXML(TO_PARSE)					# parse xml file
	saveQuestionsToCSV(newQuestions, 'questions2.csv')			# store news items in a csv file
	newAnswers = parseAnswersXML(TO_PARSE)						# parse xml file
	saveAnswersToCSV(newAnswers, 'answers2.csv')				# store news items in a csv file

	savetoCSV(newsitems, 'questions.csv')
	savetoCSV2(newsitems2, 'answers.csv')

if __name__ == "__main__":
	main()
