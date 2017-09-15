# Stdlib imports
import urllib3
import os
import json
from datetime import datetime, timedelta

# Third-party app imports
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from gcloud import datastore

# Setup datastore connection for Google Cloud
client = datastore.Client('newsai-1166')

query = client.query(kind='Email')
query.add_filter('IsSent', '=', True)
query.add_filter('Cancel', '=', False)
query.add_filter('Delievered', '=', False)

for email in query.fetch():
	if email['SendAt'].year > 2000:
		print email['SendAt']
		print email['SendGridId']

		if email['SendGridId'] != '':
			email['Delievered'] = True
