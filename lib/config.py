import json

class Watch:
    # watchtype = ""
    def a(self):
        pass

class Config:
    watches = []
    def __init__(self, configPath):
        with open (configPath) as ff:
            cfg_json = json.load(ff)
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
            self.watches.append(newwatch)

