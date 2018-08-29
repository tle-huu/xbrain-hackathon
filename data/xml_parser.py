#Python code to illustrate parsing of XML files
# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET
import sys


def cleanhtml(raw_html):
	cleantext = BeautifulSoup(raw_html, "html.parser").text

	# cleanr = re.compile('<.*?>')
	# cleantext = re.sub(cleanr, '', raw_html)
	# return cleantext

def remove_tags(text):
	return ''.join(xml.etree.ElementTree.fromstring(text).itertext())

def preprocess(data):
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
	# Step 2: tokenize
	# data = nltk.word_tokenize(data)
	# Step 3: strip stopwords
	# stemmer = snowballstemmer.stemmer('english')
	# data = stemmer.stemWords(data)

	return data

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

		data = item.attrib['title']
		data = preprocess(data)
		news['title'] = data
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


def main():
	# parse xml file
	newsitems = parseXML('train.xml')
	newsitems2 = parseXML2('train.xml')

	savetoCSV(newsitems, 'questions.csv')
	savetoCSV2(newsitems2, 'answers.csv')

if __name__ == "__main__":
	main()
