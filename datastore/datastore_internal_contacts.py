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
                'email': email
            }
            doc = {
                '_type': 'internal',
                '_index': 'database',
                '_id': email,
                'data': result
            }
            to_append.append(doc)

    print to_append
    res = helpers.bulk(es, to_append)

for i in range(0, 87):
    from_value = 0
    if i > 0:
        from_value = 1000*i
    contacts = es.search(index="contacts", body={}, size=1000 + from_value, from_=from_value)
    process_contacts(contacts)
