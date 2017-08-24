##this does its work as a chron job in a server. 
##We then use django's awesome orm to connect with and update our db. Magic!


from bs4 import BeautifulSoup
import urllib2, re, nltk, datetime, json


page = urllib2.urlopen('http://breitbart.com').read()
soup = BeautifulSoup(page, 'html.parser')

articles = soup.select('article h2 a')

articleInfo = []

for i, a in enumerate(articles):
	if a.string != None:
		articleInfo.append(dict())
		articleInfo[-1]['title'] = a.string
		articleInfo[-1]['link'] = a['href'] 

articlesTrump = [a for a in articleInfo if re.search(r"TRUMP|Trump|trump", a['title'])]

for a in articlesTrump:
	print a['title']

#write to file
now = datetime.datetime.now()
writefile = now.strftime("%y%m%d-%H%M") + '-bbTrumpHeadlines.json'

with open('trump_headlines/' + writefile, 'w+') as f:
	f.write(json.dumps(articlesTrump))
	f.close()




