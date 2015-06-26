import requests
import pandas as pd
from bs4 import BeautifulSoup
import string
from datetime import datetime

MAIN_DOMAIN = 'https://www.omb.gov.on.ca'
results = pd.DataFrame()

now = datetime.today()

for letter in string.uppercase:
	if letter == 'X':
		continue


	html = requests.get('https://www.omb.gov.on.ca/ecs/MuniList.aspx?n=%s'%letter).text

	soup = BeautifulSoup(html)

	table = soup.find_all('table')[0]
	a_list = table.find_all('a')

	urls = []
	cities = []

	for a_tag in a_list:
		url = a_tag.attrs['href']
		print MAIN_DOMAIN + url
		urls.append(MAIN_DOMAIN + url)
		cities.append(a_tag.text)

	columns = ['Property Address', 'Data Information', 'Case Description', 'Status', 'Case Number']

	for url, city in zip(urls, cities):
		tables = pd.read_html(url, skiprows=2, header=0)

		if len(tables) > 0:
			cases = tables[0][columns]
			cases['City'] = city
			print cases.shape
			print url

			results = results.append(cases)
			print results.shape

results.to_csv('omb_cases_%s%.csv'%now.strftime('%Y-%m-%d-%H'), index=False)

