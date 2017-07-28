# Stdlib imports
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

contacts = es.search(index='md', doc_type='contacts', size=1000)
for contact in contacts['hits']['hits']:
    for index, beat in enumerate(contact['_source']['data']['writingInformation']['beats']):
        if beat == 'Tech':
            contact['_source']['data']['writingInformation'][
                'beats'][index] = u'Technology'

    # Edge case in one of the contacts
    if len(contact['_source']['data']['writingInformation']['beats']) == 2:
        print contact['_id']
        print contact['_source']['data']['writingInformation']['beats']
        contact['_source']['data']['writingInformation']['beats'] = [
            contact['_source']['data']['writingInformation']['beats'][0]]
        print contact['_source']['data']['writingInformation']['beats']

    # print contact['_source']['data']['writingInformation']['beats']
    # print {
        # 'doc': {'data': {'writingInformation': {'beats': contact['_source']['data']['writingInformation']['beats']}}}}

    es.update(index='md', doc_type='contacts', id=contact['_id'], body={
        'doc': {'data': {'writingInformation': {'beats': contact['_source']['data']['writingInformation']['beats']}}}})
