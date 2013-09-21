import json
import pdb

class Alert:
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
        for alert in alerts:
            # parse the watch seciton of the alert
            watch = alert["watch"]
            newalert = Alert()
            newalert.watchtype = watch["type"]
            schedule = watch["schedule"]
            newalert.scheduletype = schedule["type"]
            newalert.scheduledays = []
            for day in schedule["days"]:
                newalert.scheduledays.append(day)
            newalert.trip = watch["trip"]
            newalert.scheduled_time = watch["scheduled-time"]
            newalert.watch_feed_name = watch["watch-feed-name"]

            # parse the action section of the alert
            action = alert["action"]
            newalert.actiontype = action["type"]
            if newalert.actiontype == "email":
                newalert.actionemailaddress = action["emailaddress"]
            self.watches[alert["alertname"]] = newalert
        
        # read in the feeds
        for f in cfg_json["feeds"]:
            feed = Feed()
            feed.feedname = f["feedname"]
            feed.feedurl = f["feedurl"]
            self.feeds.append(feed)

