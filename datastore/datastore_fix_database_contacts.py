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

page = es.search(
    index='database',
    doc_type='contacts',
    scroll='2m',
    search_type='scan',
    size=1000,
    body={}
)

sid = page['_scroll_id']
scroll_size = page['hits']['total']

# while (scroll_size > 0):
page = es.scroll(scroll_id=sid, scroll='2m')
sid = page['_scroll_id']
scroll_size = len(page['hits']['hits'])

# for x in page['hits']['hits']:
    # print x
