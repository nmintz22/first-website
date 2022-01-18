from flask import Flask, render_template, redirect, url_for, request
from bs4 import BeautifulSoup
import requests
import re
from tabulate import tabulate
from Fighter import Fighter
from fighters import getFullDictionary, getDictionaryByChar, getFighterLink
import random

#fix korean zombie link when on other fighters records (ie. ortega)

app = Flask(__name__)
app.config['SECRET_KEY'] = "jkdsghsh;gjfdjgk"


@app.route('/bulk')
def start():
	#from fighters import getFullDictionary
	global fdic
	fdic = getFullDictionary()
	return redirect(url_for("search"))
	

@app.route('/', methods=['POST','GET'])
@app.route('/search', methods=['POST','GET'])
def search():
	#from fighters import getDictionaryByChar

	if request.method == 'POST':
		f_name = request.form['query']

		f_name = str(f_name).lower()

		char = f_name[f_name.index(' ')+1:f_name.index(' ')+2]

		#global fdic
		#fdic = getDictionaryByChar(char)

		#return fdic.get(f_name)
		return redirect(url_for("record",f_name=f_name))
	else:
		return render_template("ufcsearch.html")

@app.route('/event/<show>')
def show(show):
	fights = []

	url_to_scrape = "http://ufcstats.com/statistics/events/completed?page=all"
	def getHTMLdocument(url):
		response = requests.get(url)
		return response.text

	html_document = getHTMLdocument(url_to_scrape)

	soup = BeautifulSoup(html_document, 'html.parser')
	def get_event_link():
		st = ""
		for link in soup.find_all('a', href=True):
			if str(link.text).lower().strip() == show.lower():
				st = link['href']
				break

		return st

	#links = links[5:]
	event_link = get_event_link()

	html_document2 = getHTMLdocument(event_link)

	soup2 = BeautifulSoup(html_document2, 'html.parser')

	full_list = []
	for l in soup2.find_all('a', href=True):
		full_list.append(str(l.text).strip())
		
	new_full_list = full_list[4:]
	new_full_list = new_full_list[:-6]
	fight=[]
		
	fight.append(new_full_list[1])
	fight.append(new_full_list[2])

	fights.append(fight)
	#return full_list[1]
	while len(new_full_list) > 0:
		new_full_list = new_full_list[3:]
		fight_l=[]

		try:
			fight_l.append(new_full_list[1])
			fight_l.append(new_full_list[2])
		except:
			pass

		fights.append(fight_l)
	#return str(soup2.find_all('p'))
	ps = []
	belts = 0
	for ptag in soup2.find_all('p'):
		ps.append(ptag.text.strip())

	for ii in soup2.find_all('img',src=True):
		if ii['src'] == 'http://1e49bc5171d173577ecd-1323f4090557a33db01577564f60846c.r80.cf1.rackcdn.com/belt.png':
			belts += 1

	outcomes = []
	weights = []
	time_left = []
	round_num = []
	c = 0
	for out in ps:
		if len(out) != 0:
			if out == "U-DEC" or out == "S-DEC" or out == "KO/TKO" or out == "SUB" or out == "M-DEC" or out == "DQ" or out == "CNC":
				outcomes.append(out)
			elif 'weight' in out:
				weights.append(out)
			elif ":" in out:
				round_num.append(ps[c-1][0])
				time_left.append(out)
		c +=1

	#return str(fights)

	counter = 0
	for f in fights:
		try:
			f.append(weights[counter])
			f.append(outcomes[counter])
			f.append(round_num[counter])
			f.append(time_left[counter])
		except:
			pass
		counter+=1

	fights.pop()

	for b in fights:
		if belts > 0:
			b.append('Belt')
			belts-=1
		else:
			b.append('Non-Belt')

	return render_template("showdisplay.html", show_name=show, fights=fights, event_link=event_link)

@app.route('/<f_name>')
def record(f_name):
	selected_fighter = f_name

	char = f_name[f_name.index(' ')+1:f_name.index(' ')+2]

	bundle = getFighterLink(str(f_name).lower())

	if bundle[0] == 'DNE':
		return redirect(url_for('search'))

	url_to_scrape = bundle[0]

	nickname = bundle[1]

	def getHTMLdocument(url):
		response = requests.get(url)
		return response.text

	html_document = getHTMLdocument(url_to_scrape)

	soup = BeautifulSoup(html_document, 'html.parser')

	values = []
	for link in soup.find_all('a'):
		s = link.text
		values.append(s.split())

	ps = []
	for txt in soup.find_all('p'):
		t = txt.text
		ps.append(t.split())

	ps = ps[9:]
	#return str(ps)
	outcomes = []
	round_num = []
	time_left = []
	c = 0
	for out in ps:
		if len(out) != 0:
			if out[0] == "U-DEC" or out[0] == "S-DEC" or out[0] == "KO/TKO" or out[0] == "SUB" or out[0] == "M-DEC" or out[0] == "DQ" or out[0] == "CNC":
				outcomes.append(out[0])
			elif ":" in out[0]:
				round_num.append(ps[c-1][0])
				time_left.append(out[0])
			
		
		c += 1

	values = values[4:]
	
	if(values[0][0] == 'next'):
		values = values[:3] + values[4:]
		outcomes = [' '] + outcomes
		round_num = [' '] + round_num
		time_left = [' '] + time_left
	
	values = values[:-6]

	def event_string(event):
		s = ""
		for e in event:
			s += " " + e

		return s.strip()
	

	fights = []
	i = 0
	while len(values) >= 0:
		try:
			fight = [
				values[0][0],
				values[1][0] + " " + values[1][1],
				values[2][0] + " " + values[2][1],
				outcomes[i],
				round_num[i],
				time_left[i],
				event_string(values[3])
			]

			fights.append(fight)
		except:
			break
		values = values[4:]
		i+=1

	wins = 0
	losses = 0
	draws = 0
	nc = 0
	for element in fights:
		if element[0] == 'win':
			wins+=1
		elif element[0] == 'loss':
			losses +=1
		elif element[0] == 'draw':
			draws += 1
		elif element[0] == 'nc':
			nc += 1


	name = f_name[:f_name.index(' ')] + "-" + f_name[f_name.index(' ')+1:]

	if name == 'chan-sung jung':
		url_to_scrape2 = "http://ufc.com/athlete/chan-sung-jung"
	else:
		url_to_scrape2 = "http://ufc.com/athlete/" + name

	html_document2 = getHTMLdocument(url_to_scrape2)

	soup2 = BeautifulSoup(html_document2, 'html.parser')

	imgs = []
	for img in soup2.find_all('img'):
		s = img['src']
		imgs.append(s)

	img = imgs[-5]

	url_to_scrape3 = "https://www.espn.com/mma/story/_/id/14947566/current-all-ufc-champions"

	html_document3 = getHTMLdocument(url_to_scrape3)

	soup3 = BeautifulSoup(html_document3, 'html.parser')

	lll = []
	for ll in soup3.find_all('a'):
		lll.append(str(ll.text).lower())

	index = 0
	for y in lll:
		if y == 'click here':
			lll = lll[index+1:]
		else:
			index+=1

	champions = []
	ii = 0
	for ch in lll:
		if "(" in ch:
			print(ch)
			champions.append(lll[ii+1])
			ii+=1
		else:
			ii+=1

	return render_template("ufcrecord.html", champions=champions, fighter_link=bundle[0],nickname=nickname, img=img, record=fights, wins=wins, losses=losses, draws=draws, nc=nc, fighter_name=f_name.upper())

if __name__ == '__main__':
	app.run(debug=True)





