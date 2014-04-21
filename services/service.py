import urllib, urllib.request, re, os

class Service:

    # Initialise the service
    def __init__(self, folder):
        # Set the folder name
        self.folder = folder

        #Create an array to hold picture urls
        self.picUrls = []

        # Make the directories if we can
        try:
            os.makedirs(self.folder)
        except OSError:
            pass

    # Function to download content from an url
    def openUrl(self, url):
        # Create a buffer variable
        buf = ""

        # Try to optn the url
        try:
            f       = urllib.request.urlopen(url)

        # If we get a 404 error we just skip the download
        except urllib.request.URLError:
            pass

        # Read the html content into the buffer
        else:
            buf     = f.read()
            f.close()

        # return the buffer
        return buf

    # Set the url into a local variable
    def setUrl(self, url):
        self.url = url

    # Saves the img / vid to a local file
    def savePicture(self, url, fullUrl):
        if url:
            # Find a matching url
            m = re.match(self.htmlPic, url, re.M|re.I)

            # If we have a match
            if m:
                # Set the filename
                filename = m.group(1)

                # Check if we already have the file
                if os.path.exists("%s/%s" % (self.folder,filename)) == False:

                    # Open a file to write into
                    f = open("%s/%s" % (self.folder,filename), 'wb')

                    # See if we can read the file
                    try:
                        picLink = urllib.request.urlopen(url).read()

                    # If we get a 404 then ignore
                    except urllib.request.URLError:
                        pass

                    # Write the contents of the img / vid to a local file
                    else:
                        f.write(picLink)

                    # Close the local file
                    f.close()
    
    # Creates the correct url to hunt down
    def createPicUrl(self, shortUrl):
        if self.postRegUrl:
            return self.postRegUrl % shortUrl
        else:
            return shorturl

    # Hunt for the link to the img / vid file
    def picFromHtml(self, url):
        # Open the content of the url
        content = self.openUrl(url)

        # Make sure we have real content that can be decoded
        if hasattr(content, 'decode'):

            # Search the content for the given htmlUrl and return the file name
            m = re.search(self.htmlUrl, content.decode("utf-8"), re.M|re.I)
            if m:
                return m.group()
        else:
            return ""

    # Function called when the content of the page has been downloaded
    def hunt(self, content):
        # Search the content for the given service Regexp linking to the service page
        m = re.findall(self.regexp, content.decode("utf-8"), re.M|re.I)

        # If we find a service link
        if m:
            for i in m:
                # Hunt for the link to the img / vid file
                d = self.picFromHtml(self.createPicUrl(i))

                # Save the img / vid to the local file system
                self.savePicture(d,self.createPicUrl(i))

        # Returns the amount of img / vids found
        return len(self.picUrls)

# Create a service for TwitPic
class TwitPic(Service):
    regexp     = r'pic\.twitter\.com\\\/([a-zA-Z0-9]+)\\u003c'
    htmlUrl    = r'https://pbs\.twimg\.com/media/([a-zA-Z0-9_-]+)\.jpg'
    htmlPic    = r'https://pbs\.twimg\.com/media/(.*)'
    postRegUrl = 'http://pic.twitter.com/%s'
    pass

# Create a service for Instagram
class Instagram(Service):
    regexp     = r'url=\\"http:\\\/\\\/instagram\.com\\\/p\\\/([a-zA-Z0-9]+)\\\/'
    htmlUrl    = r'http://distilleryimage[0-9]+\.ak\.instagram\.com/([a-zA-Z0-9_-]+)\.jpg'
    htmlPic    = r'http://distilleryimage[0-9]+\.ak\.instagram\.com/(.*)'
    postRegUrl = 'http://instagram.com/p/%s'
    pass

# Create a service for Vine
class Vine(Service):
    regexp     = r'vine\.co\\\/v\\/([a-zA-Z0-9]+)\\u003c'
    htmlUrl    = r'https://v\.cdn\.vine\.co/r/videos/([a-zA-Z0-9_.-]+)\.mp4'
    htmlPic    = r'https://v\.cdn\.vine\.co/r/videos/(.*)'
    postRegUrl = 'http://vine.co/v/%s'
    pass
