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


def sync_list_contacts():
    query = client.query(kind='MediaList')
    for media_list in query.fetch():
        if 'Contacts' in media_list:
            for contact_id in media_list['Contacts']:
                key = client.key('Contact', int(contact_id))
                contact = client.get(key)

                post_data = {}
                post_data['listid'] = int(media_list.key.id)

                # Post data
                json_data = json.dumps(post_data)
                r = requests.patch(
                    'https://tabulae.newsai.org/api/contacts/' + str(contact_id), data=json_data, verify=False, auth=('jebqsdFMddjuwZpgFrRo', ''))
                if r.status_code != requests.codes.ok:
                    print r.text

sync_list_contacts()
