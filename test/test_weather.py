import chiller.weather as weather
import pytest
from icecream import ic

@pytest.fixture
def weather1():
    filename = 'test/test_weather_data_1.csv'
    with open(filename, newline='') as csvfile:
        w = weather.Weather(csvfile)
    return w

def test_initialization():
    file = "test/test_weather_data_1.csv"
    with open(file, newline='') as csvfile:
        w = weather.Weather(csvfile)
    assert True

def test_weather_data_read(weather1):
    assert len(weather1.temps) == 23

def test_weather_data_read_2(weather1):
    assert weather1.temps[0] == 10

def test_NOAA_string_parse():
    string = '01-01T01:00:00'
    parsed = weather.parse_NOAA_datetime_string(string)
    assert parsed.day == 1
    assert parsed.month == 1
    assert parsed.hour == 1
    assert parsed.minute == 0
    assert parsed.second == 0

def test_seconds_between_dates():
    date1 = weather.parse_NOAA_datetime_string('01-01T01:00:00')
    date2 = weather.parse_NOAA_datetime_string('01-01T01:01:00')
    assert weather.seconds_between(date1, date2) == 60

def test_seconds_between_dates_2():
    date1 = weather.parse_NOAA_datetime_string('01-01T01:00:00')
    date2 = weather.parse_NOAA_datetime_string('01-01T02:00:00')
    assert weather.seconds_between(date1, date2) == 3600

def test_matches_data_point(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T02:00:00')
    assert weather1.matches_data_point(date) == True

def test_does_not_match_data_point(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T02:10:00')
    assert weather1.matches_data_point(date) == False

def test_temp_at_time_at_data_point(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T02:00:00')
    temp = weather1.temp_at_datetime(date)
    assert temp == 20

def test_matching_date_index(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T02:00:00')
    index = weather1.matching_date_index(date)
    assert index == 1

def test_start_date(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T01:00:00')
    assert weather1.start_date == date

def test_end_date(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T23:00:00')
    assert weather1.end_date == date

def test_within_date_data(weather1):
    date = weather.parse_NOAA_datetime_string('02-01T23:00:00')
    assert weather1.within_date_data(date) == False

def test_within_date_data(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T23:00:00')
    assert weather1.within_date_data(date) == True

def test_temp_between_data_points_1(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T01:30:00')
    temp = weather1.temp_at_datetime(date)
    assert temp == 15

def test_temp_between_data_points_2(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T06:10:00')
    temp = weather1.temp_at_datetime(date)
    assert temp == 35

def test_prior_datetime_index(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T01:15:00')
    prior_date = weather.parse_NOAA_datetime_string('01-01T01:00:00')
    assert weather1.prior_date_index(date) == 0

def test_prior_datetime(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T01:15:00')
    prior_date = weather.parse_NOAA_datetime_string('01-01T01:00:00')
    assert weather1.prior_date(date) == prior_date

def test_next_datetime_index(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T01:15:00')
    next_date = weather.parse_NOAA_datetime_string('01-01T02:00:00')
    assert weather1.next_date_index(date) == 1

def test_next_datetime(weather1):
    date = weather.parse_NOAA_datetime_string('01-01T01:15:00')
    next_date = weather.parse_NOAA_datetime_string('01-01T02:00:00')
    assert weather1.next_date(date) == next_date
