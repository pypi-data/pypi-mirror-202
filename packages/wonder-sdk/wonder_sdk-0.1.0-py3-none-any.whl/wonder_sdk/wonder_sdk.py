import time
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import pubsub_v1, storage, translate_v2

from .wonder_sdk_config import WonderSdkConfig

class WonderSdk:
    def __init__(self, config: WonderSdkConfig, app_credentials=None):
        self._config = config

        self._firebase_cred = credentials.Certificate(app_credentials) if app_credentials else credentials.ApplicationDefault()
        firebase_admin.initialize_app(self._firebase_cred, {
            'projectId': self._config.project_id
        })

    # FIRESTORE
    def get_firestore_client(self):
        if not hasattr(self, 'db'):
            self.db = firestore.client()

        return self.db

    def set_firestore_data(self, collection_name, document_name, data):
        db = self.get_firestore_client()
        doc_ref = db.collection(collection_name).document(document_name)
        doc_ref.set(data)

    def get_firestore_data(self, collection_name, document_name):
        db = self.get_firestore_client()
        doc_ref = db.collection(collection_name).document(document_name)
        doc = doc_ref.get()
        return doc.to_dict()

    # PUB/SUB
    def subscribe_to_pubsub(self, max_messages: int, callback, timeout=None):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(self._config.project_id, self._config.subscription_name)
        flow_control = pubsub_v1.types.FlowControl(max_messages=max_messages)

        def on_message(message):
            try:
                callback(message.data.decode('utf-8'))
                message.ack()
            except:
                message.ack()

        streaming_pull_future = subscriber.subscribe(subscription_path, callback=on_message, flow_control=flow_control)

        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely, unless an exception is encountered first.
                streaming_pull_future.result(timeout=timeout)
            except Exception as e:
                streaming_pull_future.cancel() # Trigger the shutdown.
                streaming_pull_future.result() # Block until the shutdown is complete.

    # TRANSLATION
    def _get_translate_client(self):
        if not hasattr(self, 'translate_client'):
            self.translate_client = translate_v2.Client()

        return self.translate_client

    def translate_text(self, text, target_language='en'):
        client = self._get_translate_client
        try:
            result = client.translate(text, target_language=target_language)
            return result['translatedText']
        except:
            return text

    # async def upload_file_to_bucket(self, bucket_name, source_file_path, destination_blob_name):
    #     storage_client = storage.Client()
    #     bucket = storage_client.bucket(bucket_name)
    #     blob = bucket.blob(destination_blob_name)
    #     await blob.upload_from_filename(source_file_path)

    # async def download_file_from_bucket(self, bucket_name, source_blob_name, destination_file_path):
    #     start_time = time.monotonic()
    #     storage_client = storage.Client()
    #     bucket = storage_client.bucket(bucket_name)
    #     blob = bucket.blob(source_blob_name)
    #     await blob.download_to_filename(destination_file_path)
    #     end_time = time.monotonic()
    #     print(f"download_file_from_bucket took {end_time - start_time:.5f} seconds")