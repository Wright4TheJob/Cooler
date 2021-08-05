from datetime import datetime
from datetime import timedelta
from cooler import utilities as utils

class Weather():
    def __init__(self, file):
        import csv
        self.time_strings = []
        self.datetimes = []
        self.temps = []
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            self.time_strings.append(row[0])
            self.temps.append(float(row[1]))
        self.datetimes = [parse_NOAA_datetime_string(d) for d in self.time_strings]
        self.start_date = min(self.datetimes)
        self.end_date = max(self.datetimes)

    def temp_at_datetime(self, datetime):
        if not self.within_date_data(datetime):
            raise ValueError('Date provided outside of date range in data file.')

        if self.matches_data_point(datetime):
            i = self.matching_date_index(datetime)
            return self.temps[i]
        else:
            prior_date = self.prior_date(datetime)
            prior_temp = self.temps[self.prior_date_index(datetime)]
            next_date = self.next_date(datetime)
            next_temp = self.temps[self.next_date_index(datetime)]
            range_seconds = seconds_between(next_date, prior_date)
            elapsed_seconds = seconds_between(datetime, prior_date)
            return utils.linear_interpolate(elapsed_seconds, 0, range_seconds, prior_temp, next_temp)

    def matches_data_point(self, datetime):
        for d in self.datetimes:
            if d == datetime:
                return True
        return False

    def matching_date_index(self, date):
        return self.datetimes.index(date)

    def within_date_data(self, date):
        if self.start_date <= date <= self.end_date:
            return True
        return False

    def prior_date_index(self, date):
        for i in range(0,len(self.datetimes)):
            if self.datetimes[i] < date < self.datetimes[i+1]:
                return i

    def prior_date(self, date):
        return self.datetimes[self.prior_date_index(date)]

    def next_date_index(self, date):
        for i in range(0,len(self.datetimes)):
            if self.datetimes[i] < date < self.datetimes[i+1]:
                return i +1

    def next_date(self, date):
        return self.datetimes[self.next_date_index(date)]


def parse_NOAA_datetime_string(string, year=2010):
    first_split = string.split('T')
    date_string = first_split[0]
    time_string = first_split[1]

    date_split = date_string.split('-')
    month = int(date_split[0])
    day = int(date_split[1])

    time_split = time_string.split(':')
    hour = int(time_split[0])
    min = int(time_split[1])
    sec = int(time_split[2])
    this_datetime = datetime(year, month, day, hour, min, sec)
    return this_datetime

def seconds_between(dt1, dt2):
    delta = dt2 - dt1
    return delta.total_seconds()
