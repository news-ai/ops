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


def get_emails_sent_today(method, id_name):
    date_from = moment.now().locale("US/Eastern").timezone("Europe/London").subtract(days=100).replace(
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
                }, {
                    'term': {
                        'data.Method': method
                    }
                }, {
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

    if id_name != '':
        query['query']['bool']['must_not'].append({'term': {id_name: ''}})

    res = es.search(index='emails2', doc_type='email', body=query)
    return res

# emails = get_emails_sent_today('sendgrid', 'data.SendGridId')
# emails = get_emails_sent_today('gmail', 'data.GmailId')
# emails = get_emails_sent_today('outlook', '')
# emails = get_emails_sent_today('smtp', '')

sent = len(emails['hits']['hits'])
opened = 0

for email in emails['hits']['hits']:
    if email['_source']['data']['Opened'] > 0:
        opened += 1

if sent > 0:
    print sent
    print opened
    print ('sengrid', (float(opened)/float(sent))*100)
else:
    print 'No emails'