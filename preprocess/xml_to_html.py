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
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

TO_PARSE = 'train.xml'

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
		news['text'] = item.attrib['text']
		newsitems.append(news)
	return newsitems

def saveAnswersToCSV(newsitems, filename):
	fields = ['id', 'group', 'elected', 'text']					# specifying the fields for csv file
	with open(filename, 'w') as csvfile:						# writing to csv file
		writer = csv.DictWriter(csvfile, fieldnames = fields)	# creating a csv dict writer object
		writer.writeheader()									# writing headers (field names)
		writer.writerows(newsitems)								# writing data rows


if __name__ == "__main__":
		newAnswers = parseAnswersXML(TO_PARSE)						# parse xml file
		saveAnswersToCSV(newAnswers, 'answershtml.csv')				
