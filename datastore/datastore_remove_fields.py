from gcloud import datastore

client = datastore.Client('newsai-1166')

kinds = [
    'User',
]

removal_fields = [
    'agreetermsandconditions',
    'apikey',
    'confirmationcode',
    'created',
    'createdby',
    'email',
    'emailconfirmed',
    'employers',
    'firstname',
    'googleid',
    'isadmin',
    'lastloggedin',
    'lastname',
    'linkedinauthkey',
    'linkedinid',
    'password',
    'resetpasswordcode',
    'updated',
]

for kind in kinds:
    query = client.query(kind=kind)

    results = []
    for result in query.fetch():
        results.append(result)

    for result in results:
        for single_key in result.keys():
            if single_key in removal_fields:
                del result[single_key]
        print result
        client.put(result)
