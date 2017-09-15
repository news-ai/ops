from gcloud import datastore

client = datastore.Client('newsai-1166')

query = client.query(kind='Contact')

# contacts = list(query.fetch())

# for contact in contacts:
#     print contact.key
#     client.delete(contact.key)

count = 0

for result in query.fetch():
    count += 1
    print count
    if 'ListId' not in result:
        print result
        # client.delete(result.key)