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


def format_organizations(email, organizations):
    all_organizations = []

    for organization in organizations:

        if 'name' in organization and organization['name'] != '':
            org_id = re.sub('[^a-zA-Z ]', '', organization['name'])
            org_id = org_id.lower()
            org_id = org_id.replace(" ", "-")
            object_index_name = email + '-' + org_id
            single_organization = {
                '_id': object_index_name,
                'email': email,
                'organizationName': organization['name'],
                'title': organization['title'] if 'title' in organization else '',
                'current': organization['current'] if 'current' in organization else False,
            }
            print single_organization

    return all_organizations


def get_contacts():
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
    # sid = page['_scroll_id']
    # scroll_size = len(page['hits']['hits'])

    for contact in page['hits']['hits']:
        if '_source' in contact and 'data' in contact['_source'] and 'organizations' in contact['_source']['data']:
            organizations = contact['_source']['data']['organizations']
            if len(organizations) > 0:
                contact_organizations = format_organizations(
                    contact['_id'], contact['_source']['data']['organizations'])
                print contact['_id'], contact_organizations

get_contacts()
