from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os


credentials_dict = {
    'type': 'service_account',
    'client_id': os.environ['BACKUP_CLIENT_ID'],
    'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
    'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
    'private_key': os.environ['BACKUP_PRIVATE_KEY'],
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)
client = storage.Client(credentials=credentials, project='hardy-orb-254815')
bucket = client.get_bucket('bucketprescriptiva')
blob = bucket.blob('results.csv')
blob.upload_from_filename('results.csv')