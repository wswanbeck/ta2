#!/usr/bin/env python
# encoding: utf-8
import sys

from bottle import route, run, request

from lib.config import Config
from lib.feedwatcher import FeedWatcherManager

# from bottle_sqlite import SQLitePlugin
import threading
import signal
import smtplib

sqlite_db = '/tmp/ta-alerts.sqlite'
# install(SQLitePlugin(dbfile=sqlite_db))

# Globals (yuk)
theconfig = Config('conf/ws.conf')
theRESTServerHost = "localhost"
theRESTServerPort = 8080
theRESTServerUrl = "http://" + theRESTServerHost + ":" + str(theRESTServerPort) + "/watch/%s"
theFeedWatcherManager = FeedWatcherManager()
# initialize the FeedWatcherManager
theFeedWatcherManager.init(theconfig)
# start watching
theFeedWatcherManager.start()


def setup(configpath):

    # startup the REST server
    rest = RESTThread()
    rest.start()

    # subscribe to watches - this will cause FeedWatchers to call back to REST server with feed updates
    for alertname in Config(configpath).watches:
        theFeedWatcherManager.subscribe(theconfig.watches[alertname].watch_feed_name, theRESTServerUrl % alertname, alertname)

class RESTThread(threading.Thread):
    def run(self):
        run(host=theRESTServerHost, port=theRESTServerPort)


# ------- REST server --------

@route('/', method='GET')
def homepage():
    return 'Hello World'

@route('/quit', method='GET')
def quit():
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

@route('/watch/:watchname', method='POST')
def post_alert(watchname):
    try:
        # if theconfig == None:
        #     return "not yet initialized"
        thiswatch = Config('conf/ws.conf').watches[watchname]

        # conn = sqlite3.connect('/tmp/ta-alerts.sqlite')
        # c = conn.cursor()
        # c.execute("SELECT url from watches where name='%s'" % watchname)
        # thiswatch = c.fetchone()
        # conn.close()
        if thiswatch.watchtype == "vehicle-assigned":
            watchtrip = thiswatch.trip
            for message in request.json["Messages"]:
                if message["Trip"] == str(watchtrip):
                    if message["Vehicle"] != "":
                        alertmessage = "Vehicle for trip " + str(watchtrip) + " is " + message["Vehicle"]
                        print "=== alert: " + alertmessage + " ==="

                        # replace some of this stuff with configured values ___
                        session = smtplib.SMTP('smtp.gmail.com', 587)
                        session.ehlo()
                        session.starttls()
                        session.ehlo()
                        session.login('wendy.swanbeck@gmail.com', 'xtlvdsksxrihalnh')
                        headers = ["from: " + 'wendy.swanbeck@gmail.com',
                           "subject: " + "Lowell train is " + message["Vehicle"] + " [forwardtophone]",
                           "to: " + thiswatch.actionemailaddress,
                           "mime-version: 1.0",
                           "content-type: text/html"]
                        headers = "\r\n".join(headers)
                        session.sendmail('wendy.swanbeck@gmail.com', thiswatch.actionemailaddress, headers + "\r\n\r\n" + alertmessage)

                        theFeedWatcherManager.unsubscribe(thiswatch.watch_feed_name, watchname)
                        break
        elif thiswatch.watchtype == "flag-arrival":
            watchtrip = thiswatch.trip
            for message in request.json["Messages"]:
                if message["Trip"] == str(watchtrip):
                    if message["Stop"] == thiswatch.watch_feed_stop:
                        if message["Flag"] == "arr":
                            alertmessage = "Trip " + str(watchtrip) + " is now arriving at " + message["Stop"]
                            print "=== alert: " + alertmessage + " ==="

                            # replace some of this stuff with configured values ___
                            session = smtplib.SMTP('smtp.gmail.com', 587)
                            session.ehlo()
                            session.starttls()
                            session.ehlo()
                            session.login('wendy.swanbeck@gmail.com', 'xtlvdsksxrihalnh')
                            headers = ["from: " + 'wendy.swanbeck@gmail.com',
                               "subject: " + alertmessage + " [forwardtophone]",
                               "to: " + thiswatch.actionemailaddress,
                               "mime-version: 1.0",
                               "content-type: text/html"]
                            headers = "\r\n".join(headers)
                            session.sendmail('wendy.swanbeck@gmail.com', thiswatch.actionemailaddress, headers + "\r\n\r\n" + alertmessage)

                            theFeedWatcherManager.unsubscribe(thiswatch.watch_feed_name, watchname)
                            break


    except:
        print '*** exception thrown in REST server post_alert ***'

    return dict(name='watchname = ' + watchname)
                                                                                                            
    #        for alertname in cfg.watches:
    #           fm.unsubscribe(cfg.watches[alertname].watch_feed_name,"http://localhost:88/alert?alertname=" + alertname)
   
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No config file given!"
        exit()
    configpath = sys.argv[1]
    setup(configpath)

