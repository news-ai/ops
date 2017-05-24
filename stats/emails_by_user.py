# -*- coding: utf-8 -*-
# Stdlib imports
import json
import os

# Third-party app imports
import certifi
from elasticsearch import Elasticsearch, helpers

# Elasticsearch
ELASTICSEARCH_USER = os.environ['NEWSAI_ELASTICSEARCH_USER']
ELASTICSEARCH_PASSWORD = os.environ['NEWSAI_ELASTICSEARCH_PASSWORD']

# Elasticsearch setup
es = Elasticsearch(
    ['https://search1.newsai.org'],
    http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
    port=443,
    use_ssl=True,
    verify_certs=True,
    ca_certs=certifi.where(),
)

def get_emails():
    query = {
        'query': {
            'bool': {
                'must': [{
                    'term': {
                        'data.IsSent': True
                    }
                }, {
                    'term': {
                        'data.Cancel': False
                    }
                }, {
                    'term': {
                        'data.Delievered': True
                    }
                }]
            }
        }
    }

    page = es.search(
        index='emails1',
        doc_type='email',
        scroll='2m',
        search_type='scan',
        size=1000,
        body=query
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

user_to_emails = get_emails()

for user_emails in user_to_emails:
    print user_emails, len(user_to_emails[user_emails])