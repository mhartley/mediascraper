from bs4 import BeautifulSoup
import urllib2, re

def scrapeArticle(articleUrl):
	req = urllib2.Request(articleUrl, headers={'User-Agent' : "magic schoolbus"})
	page = urllib2.urlopen(req).read()
	soup = BeautifulSoup(page, 'html.parser')

	headline = soup.find('h1', { "class" : "headline__title" })
	content = soup.find('div', { "class" : "entry__text" })
	pars = content.findAll('p')
	print headline
	if pars == None and headline == None:
		return None
	else:
		return [articleUrl, headline, pars]


appendfile = open('hpdata.csv', 'a+')

with open('hp_reslinks.txt', 'r') as source:
	count = 0
	othcount = 0
	for link in source:

		### handling for links that are not to breitbart
		if re.match('^http://www.huffingtonpost.com', link) == None:
			othcount = othcount +1
		
		###if it is the right website, then scrape the page	
		else:
			try:
				link = re.sub('[\n,]', '', link)
				link = re.sub('[\n,]', '', link)
				pageVal = scrapeArticle(link)
				appendfile.write(str(pageVal[0]) + '|' + str(pageVal[1]) + '|' + str(pageVal[2]) + '\n')
				count = count + 1
			except Exception as exc:
				# print traceback.format_exc()
				print exc

	print '#### HP ARTICLE COUNT : %d ####' % count
	print '#### OTH ARTICLE COUNT : %d ####' % othcount