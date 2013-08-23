import urllib2, sys, re
import services.service as service

searchTerm = None
dataID = '0'
searchTypes = ['TwitPic', 'Instagram']

if sys.argv[1:]:
        searchTerm = sys.argv[1]

searchTerm = urllib2.quote(searchTerm)

class TweetScrape:
    content = ""
    searchTerm = ""
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm
        self.content = self.openUrl(self.searchTerm)
        self.getImageShorts(self.content)
        self.nextData(self.content)

    def nextData(self, content):
        global dataID
        oldID = dataID
        tempHold = []
        m = re.findall(r'data-tweet-id=\\"([0-9]+)\\"', content, re.M|re.I)
        for i in m:
            tempHold.append(int(i))
        print tempHold
        dataID = tempHold[len(tempHold)-1]
        print ""

    def getImageShorts(self, content):
        global searchTypes
	for t in searchTypes:
            tr = getattr(service, t)('images/%s' % self.searchTerm)
            tr.hunt(self.content)

    def openUrl(self, term, page=0):
        global dataID
        baseUrl = "https://twitter.com/i/search/timeline?mode=realtime&src=typd&include_available_features=1&include_entities=1&max_id=%s&q=%s" % (dataID,term)
        print "Searching for images using term %s." % searchTerm
        print "Using web address : %s" % baseUrl
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            f = opener.open(baseUrl)
        except TypeError:
            pass
        else:
            buf     = f.read()
            f.close()
        return buf

while 1:
    tt = None
    tt = TweetScrape(searchTerm)
