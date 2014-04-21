
import urllib, urllib.request, json, sys, cgi, re
import services.service as service
import threading

searchTerm = None
dataID = '0'
scroller = ''
currentPage = 1

searchTypes = ['TwitPic', 'Instagram']

#if sys.argv[1:]:
#        searchTerm = sys.argv[1]

#searchTerm = urllib.parse.quote(searchTerm)

class TweetScrape:
    content = ""
    searchTerm = ""
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm
        self.content = self.openUrl(self.searchTerm)
        self.getImageShorts(self.content)
        self.nextData(self.content)

    def nextData(self, content):
        global dataID, scroller
        oldID = dataID
        tempHold = []
        m = re.findall(r'data-tweet-id=\\"([0-9]+)\\"', content.decode("utf-8"), re.M|re.I)
        for i in m:
            tempHold.append(int(i))
        try:
            dataID = tempHold[len(tempHold)-1]
        except IndexError:
            dataID = 0
            currentPage = 1
            scroller = 0
        else:
            scroller = "TWEET-%s-%s" % (dataID, tempHold[0])

    def getImageShorts(self, content):
        global searchTypes
        for t in searchTypes:
            tr = getattr(service, t)('images/%s' % self.searchTerm)

            trd = threading.Thread(target=tr.hunt, args=(self.content,))
            trd.deamon = True
            trd.start()

            #tr.hunt(self.content)

    def openUrl(self, term, page=0):
        global dataID, scroller
        baseUrl = "https://twitter.com/i/search/timeline?f=realtime&src=typd&include_available_features=1&include_entities=1&scroll_cursor=%s&q=%s" % (scroller,term)
        try:
            f = urllib.request.urlopen(baseUrl)
        except TypeError:
            pass
        else:
            buf     = f.read()
            f.close()
        return buf

while 1:
    tt = None

    input_term = input("Enter Search Term: ")
    searchTerm = urllib.parse.quote(input_term)

    print ("Searching for images using term %s." % (input_term))
    print ()

    searchTrd = threading.Thread(target=TweetScrape, args=(searchTerm,))
    searchTrd.deamon = True
    searchTrd.start()

    #tt = TweetScrape(searchTerm)
