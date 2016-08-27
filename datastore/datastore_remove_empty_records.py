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

