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

api_key = '5686291ee0c6c944'
url = "https://api.fullcontact.com/v2/person.json?email="


def email_to_full_contact(email, kwargs):
    # Check if it exists in ES first
    es_data = es.get(index="database", doc_type="contacts", id=email, ignore=[400, 404])
    if es_data['found']:
        if es_data['_source']['data']['status'] == 200:
            return (es_data, True)

    # If it doesn't exist
    if 'apiKey' not in kwargs:
        kwargs['apiKey'] = api_key
    r = requests.get(url + email, params=kwargs)
    return (json.loads(r.text), False)

def full_contact_to_es(email, result):
    to_append = []
    doc = {
        '_type': 'contacts',
        '_index': 'database',
        '_id': email,
        'data': result
    }
    to_append.append(doc)

    res = helpers.bulk(es, to_append)
    return res

def run_email(email):
    email = email.lower()
    result = email_to_full_contact(email, {})
    if not result[1]:
        if result[0]['status'] != 404:
            es_data = full_contact_to_es(email, result[0])
            print 'Contact added:', email
        else:
            print 'Contact invalid:', email

def fetch_and_run_email():
    contacts = es.search(index="contacts", body={}, size=8000, from_=2000)
    for contact in contacts['hits']['hits']:
        email = contact['_source']['data']['Email']
        email = email.lower()
        if email != '':
            result = email_to_full_contact(email, {})
            if not result[1]:
                if result[0]['status'] == 200:
                    es_data = full_contact_to_es(email, result[0])
                    print 'Contact added:', email
                else:
                    print result
                    print 'Contact invalid:', email
            else:
                print 'Contact already exists:', email
        else:
            print 'Contact does not have email', contact

def remove_202_status():
    contacts = es.search(index="database", doc_type="contacts", body={
            "query": {"match": {"data.status": 202}}}, size=1000)
    for contact in contacts['hits']['hits']:
        print contact['_source']['data']['status']
        print contact['_id']
        print es.delete(index="database", doc_type="contacts", id=contact['_id'])

# run_email('me@abhiagarwal.com')
fetch_and_run_email()
# remove_202_status()
