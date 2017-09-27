# -*- coding: utf-8 -*-
# Stdlib imports
import json
import os

# Third-party app imports
import moment
import certifi
from elasticsearch import Elasticsearch, helpers

# Elasticsearch
ELASTICSEARCH_USER = os.environ['NEWSAI_ELASTICSEARCH_USER']
ELASTICSEARCH_PASSWORD = os.environ['NEWSAI_ELASTICSEARCH_PASSWORD']

# Elasticsearch setup
es = Elasticsearch(
    ['https://search.newsai.org'],
    http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
    port=443,
    use_ssl=True,
    verify_certs=True,
    ca_certs=certifi.where(),
)


def get_emails_sent_today():
    date_from = moment.now().locale("US/Eastern").timezone("Europe/London").subtract(days=7).replace(
        hours=0, minutes=0, seconds=0).format('YYYY-MM-DDTHH:mm:ss')
    date_to = moment.now().locale(
        "US/Eastern").timezone("Europe/London").format('YYYY-MM-DDTHH:mm:ss')

    print date_from
    print date_to

    query = {
        'size': 100000,
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
                },  {
                    'range': {
                        'data.Created': {
                            'from': date_from,
                            'to': date_to
                        }
                    }
                }],
                'must_not': [{
                    'term': {
                        'data.CreatedBy': 5749563331706880
                    }
                }, {
                    'term': {
                        'data.CreatedBy': 5689413791121408
                    }
                }]
            }
        }
    }

    res = es.search(index='emails2', doc_type='email', body=query)
    return res

emails = get_emails_sent_today()

sent = len(emails['hits']['hits'])
opened = 0

for email in emails['hits']['hits']:
    if email['_source']['data']['Opened'] > 0:
        opened += 1

print sent
print opened
print ((float(opened)/float(sent))*100)