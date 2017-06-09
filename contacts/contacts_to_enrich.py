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


def sync_list_contacts(key):
    media_list_id = key
    key = client.key('MediaList', key)
    media_list = client.get(key)
    for contact in media_list['Contacts']:
        print str(contact)
        r = requests.get(
            'https://tabulae.newsai.org/api/contacts/' + str(contact) + '/enrich', verify=False, auth=('jebqsdFMddjuwZpgFrRo', ''))
        print r.status_code

    resync_path = 'https://tabulae.newsai.org/api/lists/' + str(media_list_id) + '/resync'
    print resync_path
    m = requests.get(resync_path, verify=False, auth=('jebqsdFMddjuwZpgFrRo', ''))
    print m.status_code

sync_list_contacts(6542458653507584)