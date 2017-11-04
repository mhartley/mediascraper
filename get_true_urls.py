import json, urllib2

jsonfile = open('bbsep_fb_page_posts.json', 'r+')
reslinksfile = open('reslinks.txt', 'a+')


def getResolutionURL():

	def findResolution(start):
		req = urllib2.Request(start, headers={'User-Agent' : "THE GIANT REPUBLICAN DILDO"})
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
			except urllib2.HTTPError, e:
				deadlinkcount = deadlinkcount + 1
				print e.fp.read()
			except Exception as e:
				print str(e)
	print 'dead links: %d, no links: %d' % (deadlinkcount, nolinkcount)
	print 'links harvested: %s' % str(len(reslinks))
	
getResolutionURL();

jsonfile.close()
reslinksfile.close()
