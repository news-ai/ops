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


def user_emails_to_timeseries(user_emails):
    date_to_email = {}
    for email in user_emails:
        if email['IsSent']:
            datetime_object = email['Created'][0:10]

            if datetime_object not in date_to_email:
                date_to_email[datetime_object] = {}

            # Append Opens
            if 'Opens' not in date_to_email[datetime_object]:
                date_to_email[datetime_object]['Opens'] = 0
            date_to_email[datetime_object]['Opens'] += email['Opened']

            # Append Clicks
            if 'Clicks' not in date_to_email[datetime_object]:
                date_to_email[datetime_object]['Clicks'] = 0
            date_to_email[datetime_object]['Clicks'] += email['Clicked']

            # Append Opens
            if 'Amount' not in date_to_email[datetime_object]:
                date_to_email[datetime_object]['Amount'] = 0
            date_to_email[datetime_object]['Amount'] += 1

    return date_to_email


def timeseries_to_es_data(user_id, timeseries):
    to_append = []

    for data_point in timeseries.keys():
        timeseries[data_point]['UserId'] = user_id
        timeseries[data_point]['Date'] = data_point

        doc = {
            '_type': 'useremail2',
            '_index': 'timeseries',
            '_id': str(user_id) + '-' + data_point,
            'data': timeseries[data_point]
        }

        to_append.append(doc)

    res = helpers.bulk(es, to_append)
    print res

email_dictionary = get_email_logs()
for single_key in email_dictionary.keys():
    timeseries = user_emails_to_timeseries(email_dictionary[single_key])
    es_data = timeseries_to_es_data(single_key, timeseries)
