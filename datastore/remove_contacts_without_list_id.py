from gcloud import datastore

client = datastore.Client('newsai-1166')


query = client.query(kind='Contact')
query.add_filter('ListId', '=', 0)
query.add_filter('IsMasterContact', '=', False)
contacts = list(query.fetch())

for contact in contacts:
    print contact