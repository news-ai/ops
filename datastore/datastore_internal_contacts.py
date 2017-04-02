# Stdlib imports
import urllib3
import os
import json
from datetime import datetime, timedelta

# Third-party app imports
import requests
import certifi
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from elasticsearch import Elasticsearch, helpers

# Elasticsearch
ELASTICSEARCH_USER = os.environ['NEWSAI_ELASTICSEARCH_USER']
ELASTICSEARCH_PASSWORD = os.environ['NEWSAI_ELASTICSEARCH_PASSWORD']

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


def process_contacts(contacts):
    to_append = []
    for contact in contacts['hits']['hits']:
        email = contact['_source']['data']['Email']
        if email:
            result = {
                'email': email,
                'valid': True
            }
            doc = {
                '_type': 'internal1',
                '_index': 'database',
                '_id': email,
                'data': result
            }
            to_append.append(doc)

    res = helpers.bulk(es, to_append)
    print res


def get_contacts():
    page = es.search(
        index='contacts',
        doc_type='contact',
        scroll='2m',
        search_type='scan',
        size=200,
        body={}
    )

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    while (scroll_size > 0):
        page = es.scroll(scroll_id=sid, scroll='2m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
        print "scroll size: " + str(scroll_size)

        process_contacts(page)

get_contacts()
