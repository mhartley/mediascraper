from bs4 import BeautifulSoup
import urllib2, re

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
		return [articleUrl, headline, par1]


scrapeBBarticle('http://www.breitbart.com/big-government/2017/06/21/deep-state-hillary-clinton-staffers-still-have-security-clearances-access-to-sensitive-government-information/?utm_source=facebook&utm_medium=social')
scrapeBBarticle('http://www.breitbart.com/big-government/2017/06/21/kobach-refugees-and-terrorism-a-massive-vulnerability-in-our-immigration-system-2/?utm_source=facebook&utm_medium=social')