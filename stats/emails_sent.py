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
    ['https://search.newsai.org'],
    http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
    port=443,
    use_ssl=True,
    verify_certs=True,
    ca_certs=certifi.where(),
)


def get_emails_sent():
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


def get_emails_opened():
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
                }, {
                    "range": {
                        "data.Opened": {
                            "gte": "1"
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


def get_emails_clicked():
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
                }, {
                    "range": {
                        "data.Clicked": {
                            "gte": "1"
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


def get_emails_bounced():
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
                }, {
                    'term': {
                        'data.Bounced': True
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

print get_emails_sent()['hits']['total']
print get_emails_opened()['hits']['total']
print get_emails_clicked()['hits']['total']
print get_emails_bounced()['hits']['total']
