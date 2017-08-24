import json, urllib2

jsonfile = open('bb_fb_page_posts.json', 'r+')
reslinksfile = open('reslinks.txt', 'a+')


def scrapeBBPages():

	def findResolution(start):
		req = urllib2.Request(start)
		res = urllib2.urlopen(req)
		return res.geturl()

	reslinks = []
	deadlinkcount = 0
	nolinkcount = 0
	for a in jsonfile:
		jsondata = json.loads(a)
		jsondata = jsondata['data']
		for post in jsondata:
			try:
				reslink = findResolution(post['link'])
				print reslink
				reslinksfile.write(str(reslink) + '\n')
			except KeyError:
				nolinkcount = nolinkcount + 1
				pass
			except urllib2.HTTPError:
				deadlinkcount = deadlinkcount + 1
				pass
	print 'dead links: %d, no links: %d' % (deadlinkcount, nolinkcount)
	print 'links harvested: %s' % str(len(reslinks))
	
scrapeBBPages();

jsonfile.close()
reslinksfile.close()