from bs4 import BeautifulSoup
import requests
from Fighter import Fighter
import re

#fighter_dictionary = {}

def getHTMLdocument(url):
	response = requests.get(url)
	return response.text

def getSiteURL(fighter_name):
	name = fighter_name.strip()
	#print(name)
	first_name = name[:name.index(' ')]
	last_name = name[name.index(' ')+1:]
	#print(first_name)
	#print(last_name)
	last_name_char = last_name[0]

	url = "http://ufcstats.com/statistics/fighters?char=" + last_name_char + "&page=all"
	return url

#fighter_name = str(input("Search for Fighter:")).lower()

def getFighterLink(f_name):
	f_name = str(f_name).lower()

	if f_name == 'chan sung jung':
		char = 'j'
	else:
		char = f_name[f_name.index(' ')+1:f_name.index(' ')+2]

	html_document = getHTMLdocument("http://ufcstats.com/statistics/fighters?char=" + char + "&page=all")

	soup = BeautifulSoup(html_document, 'html.parser')


	links = []
	fighter_names = []
	for link in soup.find_all('a', href=True):
		s = link.text.strip().lower()
		url = link['href']
		links.append(url)
		fighter_names.append(s)

	def clean_links(links):
		links = links[29:]
		print(str(links))
		links = links[:-8]
		#print(str(links))
		fighter_links = []
		for i in links:
			try:
				num = fighter_links.index(i)
			except ValueError as err:
				fighter_links.append(i)

		return fighter_links

	def clean_fighters(fighter_names):
		fighter_names = fighter_names[:-4]
		fighter_names = fighter_names[:fighter_names.index('1')]
		#fighter_names = fighter_names[:-15]
		fighter_names = fighter_names[fighter_names.index('z')+1:]
		#for i in fighter_names:
		#	print(i)

		return fighter_names

	fighter_urls = clean_links(links)
	names = clean_fighters(fighter_names)

	for link in fighter_urls:
		try:
			fighter = names[0] + " " + names[1]
			nname = names[2]
			#print(fighter)
			if fighter == f_name:
				bundle = [link, nname]
				return bundle
			else:
				names = names[3:]
		except:
			pass

	return ['DNE']

def getDictionaryByChar(char):
	fighter_dictionary = {}
	print("Adding all \'" + char + "\' names to dictionary")
	html_document = getHTMLdocument("http://ufcstats.com/statistics/fighters?char=" + char + "&page=all")

	soup = BeautifulSoup(html_document, 'html.parser')


	links = []
	fighter_names = []
	for link in soup.find_all('a', href=True):
		s = link.text.strip().lower()
		url = link['href']
		links.append(url)
		fighter_names.append(s)

	def clean_links(links):
		links = links[29:]
		links = links[:-16]
		#print(links)
		fighter_links = []
		for i in links:
			try:
				num = fighter_links.index(i)
			except ValueError as err:
				fighter_links.append(i)

		return fighter_links

	def clean_fighters(fighter_names):
		fighter_names = fighter_names[:-4]
		fighter_names = fighter_names[:fighter_names.index('1')]
		#fighter_names = fighter_names[:-15]
		fighter_names = fighter_names[fighter_names.index('z')+1:]
		#for i in fighter_names:
		#	print(i)

		return fighter_names

	fighter_urls = clean_links(links)
	names = clean_fighters(fighter_names)

	for link in fighter_urls:
		#print(link)
		fighter = names[0] + " " + names[1]
		names = names[3:]
		fighter_dictionary[fighter] = link

	return fighter_dictionary

def getFullDictionary():
	alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	fighter_dictionary={}
	for char in alphabet:
		print("Adding all \'" + char + "\' names to dictionary")
		html_document = getHTMLdocument("http://ufcstats.com/statistics/fighters?char=" + char + "&page=all")

		soup = BeautifulSoup(html_document, 'html.parser')


		links = []
		fighter_names = []
		for link in soup.find_all('a', href=True):
			s = link.text.strip().lower()
			url = link['href']
			links.append(url)
			fighter_names.append(s)

		def clean_links(links):
			links = links[29:]
			links = links[:-16]
			#print(links)
			fighter_links = []
			for i in links:
				try:
					num = fighter_links.index(i)
				except ValueError as err:
					fighter_links.append(i)

			return fighter_links

		def clean_fighters(fighter_names):
			fighter_names = fighter_names[:-4]
			fighter_names = fighter_names[:fighter_names.index('1')]
			#fighter_names = fighter_names[:-15]
			fighter_names = fighter_names[fighter_names.index('z')+1:]
			#for i in fighter_names:
			#	print(i)

			return fighter_names

		fighter_urls = clean_links(links)
		names = clean_fighters(fighter_names)

		for link in fighter_urls:
			#print(link)
			fighter = names[0] + " " + names[1]
			names = names[3:]
			fighter_dictionary[fighter] = link

	return fighter_dictionary



