import StringIO
import csv

class CommuterRailDisplayBoard:

    @staticmethod
    def GetDeparture(trip, csvdata):

        csvfile = StringIO.StringIO(csvdata)
        depreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in depreader:
            if row['Trip'] == trip:   # found trip
                csvfile.close()
                return row

        # no matching row found
        csvfile.close()
        return None