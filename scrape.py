
import urllib, urllib.request, json, sys, cgi, re
import services.service as service
import threading

searchTerm = None
dataID = '0'
scroller = ''
currentPage = 1

searchTypes = ['TwitPic', 'Instagram']

searchTerm = ""


#if sys.argv[1:]:
#        searchTerm = sys.argv[1]

#searchTerm = urllib.parse.quote(searchTerm)

class TweetScrape:
    content = ""
    searchTerm = ""
    dataID = '0'
    scroller = ''
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm
        self.run()

    def run(self):
        self.content = self.openUrl(self.searchTerm)
        self.getImageShorts(self.content)
        self.nextData(self.content)

    def nextData(self, content):
        global dataID, scroller
        oldID = self.dataID
        tempHold = []
        m = re.findall(r'data-tweet-id=\\"([0-9]+)\\"', content.decode("utf-8"), re.M|re.I)
        for i in m:
            tempHold.append(int(i))
        try:
            dataID = tempHold[len(tempHold)-1]
        except IndexError:
            dataID = 0
            currentPage = 1
            self.scroller = 0
        else:
            self.scroller = "TWEET-%s-%s" % (dataID, tempHold[0])
        self.run()

    def getImageShorts(self, content):
        global searchTypes, searchTrd
        for t in searchTypes:
            tr = getattr(service, t)('images/%s' % self.searchTerm)

            searchTrd = threading.Thread(target=tr.hunt, args=(self.content,))
            searchTrd.deamon = True
            searchTrd.start()

            #tr.hunt(self.content)

    def openUrl(self, term, page=0):
        global dataID, scroller
        baseUrl = "https://twitter.com/i/search/timeline?f=realtime&src=typd&include_available_features=1&include_entities=1&scroll_cursor=%s&q=%s" % (self.scroller,term)
        try:
            f = urllib.request.urlopen(baseUrl)
        except TypeError:
            pass
        else:
            buf     = f.read()
            f.close()
        return buf

def keepRunning():
    while 1:
        input_term = input("Enter Search Term: ")
        searchTerm = urllib.parse.quote(input_term)

        print ("Searching for images using term %s." % (input_term))
        print ()

        downThread = threading.Thread(target=TweetScrape, args=(searchTerm,))
        downThread.deamon = True
        downThread.start()

        #tt = TweetScrape(searchTerm)


keepRun = threading.Thread(target=keepRunning)
keepRun.deamon = True
keepRun.start()



    #tt = TweetScrape(searchTerm)