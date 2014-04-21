import urllib, urllib.request, re, os

class Service:

    def __init__(self, folder):
        self.folder = folder
        self.picUrls = []
        try:
            os.makedirs(self.folder)
        except OSError:
            pass

    def openUrl(self, url):
        buf = ""
        try:
            f       = urllib.request.urlopen(url)
        except urllib.request.URLError:
            pass
        else:
            buf     = f.read()
            f.close()
        return buf

    def setUrl(self, url):
        self.url = url

    def savePicture(self, url, fullUrl):
        if url:
            m = re.match(self.htmlPic, url, re.M|re.I)
            if m:
                filename = m.group(1)
                if os.path.exists("%s/%s" % (self.folder,filename)) == False:
                    #print ("\033[32mImage from %s saved as %s.\033[0m" % (fullUrl,filename))
                    f = open("%s/%s" % (self.folder,filename), 'wb')
                    try:
                        picLink = urllib.request.urlopen(url).read()
                    except urllib.request.URLError:
                        pass
                    else:
                        f.write(picLink)
                    f.close()
    
    def createPicUrl(self, shortUrl):
        if self.postRegUrl:
            return self.postRegUrl % shortUrl
        else:
            return shorturl

    def picFromHtml(self, url):
        content = self.openUrl(url)
        if hasattr(content, 'decode'):
            m = re.search(self.htmlUrl, content.decode("utf-8"), re.M|re.I)
            if m:
                return m.group()
        else:
            return ""

    def hunt(self, content):
        m = re.findall(self.regexp, content.decode("utf-8"), re.M|re.I)
        if m:
            for i in m:
                d = self.picFromHtml(self.createPicUrl(i))
                self.savePicture(d,self.createPicUrl(i))
        return len(self.picUrls)

class TwitPic(Service):
    regexp     = r'pic\.twitter\.com\\\/([a-zA-Z0-9]+)\\u003c'
    htmlUrl    = r'https://pbs\.twimg\.com/media/([a-zA-Z0-9_-]+)\.jpg'
    htmlPic    = r'https://pbs\.twimg\.com/media/(.*)'
    postRegUrl = 'http://pic.twitter.com/%s'
    pass

class Instagram(Service):
    regexp     = r'url=\\"http:\\\/\\\/instagram\.com\\\/p\\\/([a-zA-Z0-9]+)\\\/'
    htmlUrl    = r'http://distilleryimage[0-9]+\.ak\.instagram\.com/([a-zA-Z0-9_-]+)\.jpg'
    htmlPic    = r'http://distilleryimage[0-9]+\.ak\.instagram\.com/(.*)'
    postRegUrl = 'http://instagram.com/p/%s'
    pass
