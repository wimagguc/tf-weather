from dateutil import rrule
from datetime import datetime
import json
import requests
import os
import numpy
import sys

"""
Download weather data from Weather Company Data.

* Docs: 
  https://console.bluemix.net/docs/services/Weather/weather_rest_apis.html#rest_apis

* Test with the live endpoints:
  https://twcservice.eu-gb.mybluemix.net/rest-api/

* Naked REST urls:
  https://twcservice.eu-gb.mybluemix.net/api/weather/v1/geocode/51.500673/-0.193532/almanac/daily.json?units=m&start=1
  (Log in with username/password first)
"""


def download_weather_data(start_date, latitude, longitude, headers):
    """
    Reads values from the endpoint and prints it to the console.
    """
    base_url = os.environ['WEATHER_BASE_URL']
    username = os.environ['WEATHER_USERNAME']
    password = os.environ['WEATHER_PASSWORD']

    url = '{}/{}/{}/almanac/daily.json?units=m&start={}'.format(
        base_url, str(latitude), str(longitude), str(start_date))

    r = requests.get(url, auth=(username, password))

    try:
        json_data = r.json()
        json_data = json_data['almanac_summaries'][0]

        row_data = []
        for h in headers:
            row_data.append(json_data[h])

    except json.decoder.JSONDecodeError:
        print('JSON could not be decoded')

    return row_data


if __name__ == "__main__":
    # London
    latitude = 51.500673
    longitude = -0.193532

    headers = [
        'station_id', 'station_name', 'almanac_dt',
        'avg_hi', 'avg_lo']

    all_data = []
    all_data.append(headers)

    days_in_a_year = rrule.rrule(
        rrule.DAILY,
        dtstart=datetime.strptime('20000101', '%Y%m%d'),
        until=datetime.strptime('20000131', '%Y%m%d'))

    for dt in days_in_a_year:
        i = int(dt.strftime('%m%d'))
        row_data = download_weather_data(i, latitude, longitude, headers)
        all_data.append(row_data)

    all_data = numpy.asarray(all_data, dtype=object)
    numpy.savetxt(sys.stdout, all_data, delimiter=',', fmt='%s')

