from gcloud import datastore

client = datastore.Client('newsai-1166')


def user_to_contacts(user_id, resource):
    query = client.query(kind=resource)
    query.add_filter('CreatedBy', '=', user_id)
    resource = list(query.fetch())
    return resource


def delete_resource(resource):
    client.delete(resource.key)


def get_resource_and_delete(user_id, resource_name):
    resources = user_to_contacts(user_id, resource_name)
    print user_id, resource_name, len(resources)

    for resource in resources:
        delete_resource(resource)

user_id = 4648439698685952
get_resource_and_delete(user_id, 'Contact')
get_resource_and_delete(user_id, 'Email')

# Delete user
user_id_key = client.key('User', user_id)
client.delete(user_id_key)
