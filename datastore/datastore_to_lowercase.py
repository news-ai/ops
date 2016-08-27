from gcloud import datastore

client = datastore.Client('newsai-1166')

kinds = [
    'Agency',
    'Contact',
    'Email',
    'File',
    'MediaList',
    'Notification',
    'NotificationObject',
    'NotificationChange',
    'Publication',
    'Team',
    'Template',
    'User',
]

for kind in kinds:
    query = client.query(kind=kind)

    results = []
    for result in query.fetch():
        results.append(result)

    for result in results:
        for single_key in result.keys():
            result[single_key.lower()] = result[single_key]
            del result[single_key]
        print result
        client.put(result)
