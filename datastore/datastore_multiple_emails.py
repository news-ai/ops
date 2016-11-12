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

tags = {}

def get_contacts():
    query = client.query(kind='Contact')
    for contact in query.fetch():
        # print contact
        if 'Email' in contact:
            if contact['Email'] in tags:
                tags[contact['Email']] += 1
            else:
                tags[contact['Email']] = 1
        # print tags

get_contacts()

x = 1
print [i for i in tags if tags[i] > x]
