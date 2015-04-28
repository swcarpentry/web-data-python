import requests
import io
import csv

url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/CAN.csv'
response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    reader = io.StringIO(response.text)
    wrapper = csv.reader(reader)
    results = []
    for record in wrapper:
        if record[0] != 'year':
            year = int(record[0])
            value = float(record[1])
            results.append([year, value])
    print('first five results')
    print(results[:5])
