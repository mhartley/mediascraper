import urllib2, json
from unidecode import unidecode
#facebook access
ACCESS_TOKEN = "EAACEdEose0cBAO8ozOzZBpeXJZCDENoyyXhPRyDEPj9eRvQGhc9zkcYlahH9HjcFGZChU7Trb5oZAls3DDs8y2RXtRQXuv1DejqzYSJkspUAAd75mCzwppkQkGpQv1sm60C7daLEXqTm50enDskBEZCRQZA65wbYiNVPFOGyqEvZBXsuW2TZCyeQKdwfpJj2LUeZAS4RHXi8MhgZDZD"

request_url = "https://graph.facebook.com/v2.10/95475020353/posts?fields=message%2Clink%2Ccreated_time&limit=100&access_token=" + ACCESS_TOKEN

jsonfile = open('bb_fb_page_posts.json', 'a+')
csvfile = open('bb_fb_page_posts.csv', 'a+')

def request_fb_page_posts(graph_url):
	request = urllib2.Request(graph_url)
	response = urllib2.urlopen(request).read()  #return a json-formatted string
	data = json.loads(response)
	next = data['paging']['next']
	
	#convert loaded json to csv and write each post as a seperate record to file
	def json2csv():
		for a in data['data']:
			try:
				postrecord = str(unidecode(a['link'])) + ',' + str(unidecode(a['message'])) + ',' + str(unidecode(a['created_time'])) + '\n'
			except KeyError:
				postrecord = ',,\n'
			csvfile.write(postrecord)
	json2csv()

	#now set new request url and call function again for next page, until we get to the date we want		
	request_url = next
	last_post_date = str(data['data'][-1]['created_time'][:7])
	print 'last post date' + last_post_date
	jsonfile.write(response + '\n') ### write the response (string) not data (dict)
	if last_post_date not in ['2016-07','2016-08']:
		print '#####REQESTING NEXT#####'
		print request_url
		request_fb_page_posts(request_url)  ##recursiveness... to infinity and beyond! (not atually an infinite loop)
		#if graph api throws an error this will throw a python KeyError

	return data

jsondata = request_fb_page_posts(request_url)
	
def scrapeBBsite():
	for a in data['data']:
		




##page_posts data is pretty dirty, 18650 lines. Follow links to scrape page posts, headlines and decks
##We're only accepting data from completed rows.
##First task is to get complete url to which the posted shortened url links, then scrape



def scrapeBBPages():
	for line in jsondata:
		linksArray = [filter(lambda t: t if post['link'] != None else 0, post) for post in line['data']]
		print linksArray

scrapeBBPages();




	
		


