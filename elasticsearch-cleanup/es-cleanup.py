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

results = es.search(index='tweets', doc_type='tweet', size=1000)

count = {}
results_per_id = {}

for result in results['hits']['hits']:
    if result['_source']['data']['TweetId'] not in count:
        count[result['_source']['data']['TweetId']] = 0
        results_per_id[result['_source']['data']['TweetId']] = []
    count[result['_source']['data']['TweetId']] += 1
    results_per_id[result['_source']['data']['TweetId']].append(result)

to_append = []
for x in count:
    if count[x] > 1:
        single_result = results_per_id[x][0]
        print single_result
        doc = {
            '_type': 'tweets',
            '_index': 'tweet',
            '_id': single_result['_source']['data']['TweetId'],
            'data': single_result['_source']['data']
        }
        to_append.append(doc)
        for each_result in results_per_id[x]:
            res = es.delete(
                index='tweets', doc_type='tweet', id=each_result['_id'])
            print res

print to_append
res = helpers.bulk(es, to_append)
