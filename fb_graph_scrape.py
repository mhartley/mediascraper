import urllib2, json, csv
from unidecode import unidecode
#facebook access
ACCESS_TOKEN = 'EAACEdEose0cBAEcIgPRrEVeWVVmHoPyP65toAGcRxIPUlF0O4IBT7b4R2wMZBOm0uVE6iSJ3Np8tG56WWzUGX7s97sk689ZCofZAZBqiqhLEaF4y6N5eYQfHC4tABRZCwPZC6oP1agIfKDqUEriBSZA8yj22QFNI9vRnGDAHkXTSAsQbFtHKgEHRFoZCWszwLE8ZD'
TARGET_PAGE_ID = "95475020353"
request_url = "https://graph.facebook.com/v2.10/" + TARGET_PAGE_ID + "/posts?fields=message%2Clink%2Ccreated_time&limit=100&access_token=" + ACCESS_TOKEN

jsonfile = open('bbsep_fb_page_posts.json', 'a+')
csvfile = open('bbsep_fb_page_posts.csv', 'a+')

jsonfile.truncate()
csvfile.truncate()

def request_fb_page_posts(graph_url):
	print graph_url
	request = urllib2.Request(graph_url)
	response = urllib2.urlopen(request).read()  
	data = json.loads(response)
	next = data['paging']['next']
	
	#convert loaded json to csv and write each post as a seperate record to file
	def json2csv():
		for a in data['data']:
			try:
				postrecord = str(unidecode(a['link'])) + '|' + str(unidecode(a['message'])) + '|' + str(unidecode(a['created_time'])) + '\n'
			except KeyError:
				postrecord = ',,\n'
			csvfile.write(postrecord)
	json2csv()

	#now set new request url and call function again for next page, until we get to the date we want		
	request_url = next
	last_post_date = str(data['data'][-1]['created_time'][:7])
	print 'last post date' + last_post_date
	jsonfile.write(response + '\n') ### write the response (string) not data (dict)
	if last_post_date not in ['2017-08']:
		print '#####REQESTING NEXT#####'
		print request_url
		request_fb_page_posts(request_url)  ##recursiveness... to infinity and beyond! (not atually an infinite loop)
		#if graph api throws an error this will throw a python KeyError

	return data

jsondata = request_fb_page_posts(request_url)
		

##page_posts data is pretty dirty, 18650 lines. Follow links to scrape page posts, headlines and decks
##We're only accepting data from completed rows.
##First task is to get complete url to which the posted shortened url links, then scrape


# reslinksfile = open('hp_reslinks.txt', 'a+')



# jsonfile.read()
# def getResolutionURL():

# 	def findResolution(start):
# 		req = urllib2.Request(start)
# 		res = urllib2.urlopen(req)
# 		return res.geturl()

# 	reslinks = []
	
# 	deadlinkcount = 0
# 	nolinkcount = 0
# 	for a in jsonfile:
# 		print 'hello'
# 		jsondata = json.loads(a)
# 		jsondata = jsondata['data']
# 		for post in jsondata:
# 			try:
# 				reslink = findResolution(post['link'])
# 				print reslink
# 				reslinksfile.write(str(reslink) + '\n')
# 			except KeyError:
# 				nolinkcount = nolinkcount + 1
# 				pass
# 			except urllib2.HTTPError:
# 				deadlinkcount = deadlinkcount + 1
# 				pass
# 	print 'dead links: %d, no links: %d' % (deadlinkcount, nolinkcount)
# 	print 'links harvested: %s' % str(len(reslinks))
	

# getResolutionURL();

# jsonfile.close()
# reslinksfile.close()






	
		


