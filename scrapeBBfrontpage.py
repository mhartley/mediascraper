##this does its work as a chron job in a server. 
##We then use django's awesome orm to connect with and update our db. Magic!


from bs4 import BeautifulSoup
import urllib2, re, datetime, json
from unidecode import unidecode
# from scrapearticle import scrapeBBarticle


def scrapeBBarticle(articleUrl):
	page = urllib2.urlopen(articleUrl).read()
	soup = BeautifulSoup(page, 'html.parser')

	header = soup.find('header', { "class" : "articleheader" })
	headline = header.h1
	content = soup.find('div', { "class" : "entry-content" })
	if content.h2:
		par1 = content.h2
	else:
		par1 = content.p
	print headline
	print par1
	if par1 == None and headline == None:
		return None
	else:
		return [articleUrl, unidecode(headline), unidecode(par1)]


page = urllib2.urlopen('http://breitbart.com').read()
soup = BeautifulSoup(page, 'html.parser')

articles = soup.select('article h2 a')

articleInfo = []

for i, a in enumerate(articles):
	if a.string != None:
		articleInfo.append(dict())
		articleInfo[-1]['title'] = a.string
		articleInfo[-1]['link'] = a['href'] 

articlesTrump = [scrapeBBarticle('http://breitbart.com' + a['link']) for a in articleInfo if re.search(r"TRUMP|Trump|trump", a['title'])]

# for a in articlesTrump:
# 	print a['title']
print 'len of articlesTrump:'
print len(articlesTrump)



#write to file
now = datetime.datetime.now()
writefile = now.strftime("%y%m%d-%H%M") + '-bbTrumpHeadlines.tsv'

with open('trump_headlines/' + writefile, 'w+') as f:
	for a in articlesTrump:
		f.write(str(a[0]) + '\t' + str(a[1]) + '\t' + str(a[2]) + '\n')
	f.close()








