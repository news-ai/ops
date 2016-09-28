from gcloud import datastore

client = datastore.Client('newsai-1166')


query = client.query(kind='Contact')

# contacts = list(query.fetch())

# for contact in contacts:
#     print contact.key
#     client.delete(contact.key)

for result in query.fetch():
    if 'ListId' not in result:
        client.delete(result.key)