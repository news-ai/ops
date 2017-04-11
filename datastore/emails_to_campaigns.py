# Stdlib imports
import urllib3
import os
import re
import json
from datetime import datetime, timedelta

# Third-party app imports
import requests
import certifi
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from elasticsearch import Elasticsearch, helpers
from gcloud import datastore

# Elasticsearch
ELASTICSEARCH_USER = os.environ['NEWSAI_ELASTICSEARCH_USER']
ELASTICSEARCH_PASSWORD = os.environ['NEWSAI_ELASTICSEARCH_PASSWORD']

# Setup datastore connection for Google Cloud
client = datastore.Client('newsai-1166')

# Removing requests warning
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Elasticsearch setup
es = Elasticsearch(
    ['https://search1.newsai.org'],
    http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
    port=443,
    use_ssl=True,
    verify_certs=True,
    ca_certs=certifi.where(),
)


def get_email_logs():
    page = es.search(
        index='emails',
        doc_type='email',
        scroll='2m',
        search_type='scan',
        size=1000,
        body={}
    )

    user_to_emails = {}

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    while (scroll_size > 0):
        page = es.scroll(scroll_id=sid, scroll='2m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
        print "scroll size: " + str(scroll_size)

        for email in page['hits']['hits']:
            email_id = email['_source']['data']['CreatedBy']

            if email_id not in user_to_emails:
                user_to_emails[email_id] = []

            user_to_emails[email_id].append(email['_source']['data'])

    return user_to_emails


def user_emails_to_campaigns(user_emails):
    date_to_email = {}
    for email in user_emails:
        if email['IsSent']:
            datetime_object = email['Created'][0:10]

            if datetime_object not in date_to_email:
                date_to_email[datetime_object] = {}

            if email['Subject'] != '':
                date_to_email[datetime_object][email['Subject']] = True

    return date_to_email


def campaigns_to_es_data(user_id, campaigns):
    pattern = re.compile('([^\s\w]|_)+')
    to_append = []

    for data_point in campaigns.keys():
        for campaign in campaigns[data_point].keys():
            name = pattern.sub('', campaign)
            name = name.strip()
            name = name.replace(' ', '-')
            name = name.lower()
            doc = {
                '_index': 'emails',
                '_type': 'campaign1',
                '_id': str(user_id) + '-' + data_point + '-' + name,
                'data': {
                    'Subject': campaign,
                    'Date': data_point,
                    'UserId': str(user_id),
                }
            }

            to_append.append(doc)

    res = helpers.bulk(es, to_append)
    print res

email_dictionary = get_email_logs()
for single_key in email_dictionary.keys():
    campaigns = user_emails_to_campaigns(email_dictionary[single_key])
    es_data = campaigns_to_es_data(single_key, campaigns)
