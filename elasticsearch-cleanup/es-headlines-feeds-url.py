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
    ['https://search1.newsai.org'],
    http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
    port=443,
    use_ssl=True,
    verify_certs=True,
    ca_certs=certifi.where(),
)

results = es.search(index='feeds', doc_type='feed', size=5000)

to_append = []

for result in results['hits']['hits']:
    headlines_id = result['_id']
    headlines_data = result['_source']
    if '@' in headlines_data['data']['FeedURL']:
        headlines_data['data']['FeedURL'] = headlines_data['data']['FeedURL'].replace("@", "#40")
        doc = {
            '_type': 'feeds',
            '_index': 'feed',
            '_id': headlines_id,
            'data': headlines_data['data']
        }
        to_append.append(doc)


print to_append

res = helpers.bulk(es, to_append)

print res
