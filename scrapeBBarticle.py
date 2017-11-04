pfrom bs4 import BeautifulSoup
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


appendfile = open('bbdata.csv', 'a+')

with open('reslinks.txt', 'r') as source:
	count = 0
	othcount = 0
	for link in source:

		### handling for links that are not to breitbart
		if re.match('^http://www.breitbart.com', link) == None:
			othcount = othcount +1
		
		###if it is breitbart, then scrape the page	
		else:
			try:
				link = re.sub('[\n,]', '', link)
				pageVal = scrapeBBarticle(link)
				appendfile.write(str(pageVal[0]) + ',' + str(pageVal[1]) + ',' + str(pageVal[2]) + '\n')
				count = count + 1
			except Exception as exc:
				# print traceback.format_exc()
				print exc

	print '#### BB ARTICLE COUNT : %d ####' % count
	print '#### OTH ARTICLE COUNT : %d ####' % othcount