from time import mktime, strptime, strftime
from googlemaps import Client
from ApiKey import Key

class CommutingDurations(object):

    def __init__(self, origin, times):
        self.week = int(strftime('%W')) + 1
        self.year = strftime('%y')
        self.origin = origin
        self.times = times
        self.gmaps = Client(key=Key())
        self.durations = self.prepare_durations_dict(times)

    @staticmethod
    def get_seconds_since_epoch(self, time, weekday):
        """ Returns No. seconds since Epoch
            year: 00-99, week: 0-52, weekday: 0-6, time: 23:59 """
        return mktime(strptime("%s %d %d %s" % (time, weekday, self.week, self.year), "%H:%M %w %W %y"))

    @staticmethod
    def get_duration_from_api(self, departure_time, destination):
        """Return duration between two locations, given departure time, destination and origin"""
        api_query = self.gmaps.distance_matrix(self.origin,
                                               destination,
                                               departure_time=departure_time,
                                               mode='driving',
                                               traffic_model='pessimistic')
        duration = api_query['rows'][0]['elements'][0]['duration_in_traffic']['text']
        return duration

    def prepare_durations_dict(self, times):
        """Prepares the output dictionary containing durations"""
        durations = {}
        for keys in times:
            durations[keys]=[]
        return durations

    def calculate(self):
        """Cycles through times and destinations, storing results in a dict"""
        for destination,times in self.times.items():
            for weekday in range(0,7):
                for time in times:
                    departure_time = self.get_seconds_since_epoch(self, time, weekday)
                    duration = self.get_duration_from_api(self, departure_time, destination)
                    self.durations[destination].append(duration)
        return self.durations

"""Basic test"""
if __name__ == "__main__":
    origin = "Halifax"
    times = {"Manchester":["06:40","17:10"], "Liverpool":["06:00","15:35"]}
    test = CommutingDurations(origin, times)
    print test.calculate()


