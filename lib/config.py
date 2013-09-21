import json
import pdb

class Watch:
    # watchtype = ""
    def a(self):
        pass

class Feed:
    def a(self):
        pass


class Config:
    def __init__(self, configPath):
        self.watches = {}
        self.feeds = []

        # interpret the config file as json
        with open (configPath) as ff:
            cfg_json = json.load(ff)
        
        # read in the alerts
        alerts = cfg_json["alerts"]
        for watch in alerts:
            newwatch = Watch()
            newwatch.watchtype = watch["type"]
            schedule = watch["schedule"]
            newwatch.scheduletype = schedule["type"]
            newwatch.scheduledays = []
            for day in schedule["days"]:
                newwatch.scheduledays.append(day)
            newwatch.trip = watch["trip"]
            newwatch.scheduled_time = watch["scheduled-time"]
            newwatch.watch_feed_name = watch["watch-feed-name"]
            self.watches[watch["alertname"]] = newwatch
        
        # read in the feeds
        for f in cfg_json["feeds"]:
            feed = Feed()
            feed.feedname = f["feedname"]
            feed.feedurl = f["feedurl"]
            self.feeds.append(feed)

