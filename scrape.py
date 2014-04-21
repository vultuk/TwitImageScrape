
import urllib, urllib.request, json, sys, cgi, re
import services.service as service
import threading

# Set up the variables we may need
## Many of these are out-dated due to the new multi-threading system
searchTerm = None
dataID = '0'
scroller = ''
currentPage = 1

# Initiate the services we will search for
searchTypes = ['TwitPic', 'Instagram', 'Vine']

# Class to handle scraping
class TweetScrape:
    content = ""
    searchTerm = ""
    dataID = '0'
    scroller = ''

    # Init the class and required variables
    def __init__(self, searchTerm):
        # Store the search term requested
        self.searchTerm = searchTerm

        # Run the scraper
        self.run()

    # Function to run the scraper
    def run(self):
        # Load the required URL based on the search term
        self.content = self.openUrl(self.searchTerm)

        # Get a list of all URLS in the tweet listing and scrape them
        self.getImageShorts(self.content)

        # Move on the the next page of tweets
        self.nextData(self.content)

    # Function to move to the next page of tweets
    def nextData(self, content):
        global dataID, scroller
        oldID = self.dataID
        tempHold = []

        # Get a list of all tweet IDs that we have checked
        m = re.findall(r'data-tweet-id=\\"([0-9]+)\\"', content.decode("utf-8"), re.M|re.I)
        for i in m:
            tempHold.append(int(i))

        # Check we can get the required details to generate the next page
        try:
            dataID = tempHold[len(tempHold)-1]

        # If we get an index error then we reset to page one
        except IndexError:
            dataID = 0
            currentPage = 1
            self.scroller = 0

        # Create the details to request the next page of tweets
        else:
            self.scroller = "TWEET-%s-%s" % (dataID, tempHold[0])

        # Run the scraper
        self.run()

    # Check the page for the services we have requested
    def getImageShorts(self, content):
        global searchTypes, searchTrd
        for t in searchTypes:
            tr = getattr(service, t)('images/%s' % self.searchTerm)

            searchTrd = threading.Thread(target=tr.hunt, args=(self.content,))
            searchTrd.deamon = True
            searchTrd.start()

            #tr.hunt(self.content)

    # Get the HTML from the page of tweets
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

# Function that does the multi-threading for search terms
def keepRunning():
    # Run infinitely
    while 1:
        # Get a search term from the user
        input_term = input("Enter Search Term: ")

        # Make sure the term is safe for web
        searchTerm = urllib.parse.quote(input_term)

        # Let the user know we are working for them
        print ("Searching for images using term %s." % (input_term))
        print ()

        # Send the serch term to the Scraper in a new thread
        downThread = threading.Thread(target=TweetScrape, args=(searchTerm,))
        downThread.deamon = True
        downThread.start()


# Create the multi-threading environment to keep the service running
keepRun = threading.Thread(target=keepRunning)
keepRun.deamon = True
keepRun.start()
