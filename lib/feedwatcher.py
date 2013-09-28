import threading
import time
import urllib2

class FeedWatcherManager:

    def init(self, cfg):
        self.feedwatchers = {}
        for feed in cfg.feeds:
            self.feedwatchers[feed.feedname] = FeedWatcher(feed.feedurl, feed.feedname)

    def start(self):
        for fw in self.feedwatchers:
            self.feedwatchers[fw].start()

    def stop(self):
        for fw in self.feedwatchers:
            self.feedwatchers[fw].signalstop()

    def subscribe(self, feedname, suburl, alertname):
        self.feedwatchers[feedname].subscribe(suburl, alertname)

    def unsubscribe(self, feedname, watchname):
        self.feedwatchers[feedname].unsubscribe(watchname)

class FeedWatcher(threading.Thread):

    def __init__(self, feedurl, feedname):
        # when threadstop is True, the thread will stop
        self.threadstop = False

        # subscriber Urls
        self.subscriberUrls = {}

        threading.Thread.__init__(self)
        self.feedurl = feedurl
        self.feedname = feedname

    def signalstop(self):
        self.threadstop = True
        print "Stop watching feed: " + self.feedurl

    def run(self):
        print "Start watching feed: " + self.feedurl
        while not self.threadstop:
            # read from feedurl
            response = urllib2.urlopen(str(self.feedurl))
            self.feeddata = response.read()

            if len(self.subscriberUrls) > 0:
                self.postToSubscribers()
            time.sleep(10)

    def subscribe(self, notifySubscriberUrl, watchname):
        self.subscriberUrls[notifySubscriberUrl] = watchname
        print "subscribed: " + notifySubscriberUrl + ", alertname: " + watchname + " to feed: " + self.feedurl

    def unsubscribe(self, watchname):
        try:
            # in case caller gave us a non-existant url, assume this could fail
            for url in self.subscriberUrls:
                if self.subscriberUrls[url] == watchname:
                    self.subscriberUrls[url] = None  # no longer subscribed if the watchname is None
                    break
        except:
            pass
        print "Unsubscribed " + watchname + " to feed " + self.feedurl

    def postToSubscribers(self):
        for sub in self.subscriberUrls:
            if self.subscriberUrls[sub] != None:
                req = urllib2.Request(sub)
                req.add_header('Content-Type', 'application/json')
                try:
                    # in case something goes wrong here, we don't want to crash
                    print "posting to subscriber: " + sub + " from " + self.feedurl
                    # response = urllib2.urlopen(req, '{ "feedurl" : "' + self.feedurl + '"}')
                    response = urllib2.urlopen(req, str(self.feeddata))
                except:
                    print "*** Error during post to " + sub + " ***"
                    pass
