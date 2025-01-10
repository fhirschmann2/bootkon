#!/usr/bin/env python
# Author: Wissem Khlifi, Fabian Hirschmann
import io
import csv
import json
import avro.schema
from avro.io import BinaryEncoder, DatumWriter
from google.cloud import pubsub_v1
from google.cloud import storage
import os

project_id = os.environ['PROJECT_ID']
topic_id = "fraud-detection-topic"
bucket_name = os.environ['PROJECT_ID'] + "-bucket"
csv_folder_path = "bootkon-data/csv/ulb_fraud_detection/"
schema_file_path = "src/data_ingestion/fraud_detection_pubsub_schema.json"

# Initialize Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

# Load the AVRO schema
avro_schema = avro.schema.parse(open(schema_file_path, "rb").read())

# Pub/Sub client initialization
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def publish_avro_record(record):
    bytes_io = io.BytesIO()
    writer = DatumWriter(avro_schema)
    encoder = BinaryEncoder(bytes_io)
    writer.write(record, encoder)
    future = publisher.publish(topic_path, bytes_io.getvalue())
    return future.result()


def process_csv_blob(blob):
    temp_file_path = "/tmp/tempfile.csv"
    blob.download_to_filename(temp_file_path)


    with open(temp_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i, row in enumerate(csv_reader):
            feedback = row[-1]
            record = {
               "Time": float(row[0]),
               "V1": float(row[1]),
               "V2": float(row[2]),
               "V3": float(row[3]),
               "V4": float(row[4]),
               "V5": float(row[5]),
               "V6": float(row[6]),
               "V7": float(row[7]),
               "V8": float(row[8]),
               "V9": float(row[9]),
               "V10": float(row[10]),
               "V11": float(row[11]),
               "V12": float(row[12]),
               "V13": float(row[13]),
               "V14": float(row[14]),
               "V15": float(row[15]),
               "V16": float(row[16]),
               "V17": float(row[17]),
               "V18": float(row[18]),
               "V19": float(row[19]),
               "V20": float(row[20]),
               "V21": float(row[21]),
               "V22": float(row[22]),
               "V23": float(row[23]),
               "V24": float(row[24]),
               "V25": float(row[25]),
               "V26": float(row[26]),
               "V27": float(row[27]),
               "V28": float(row[28]),
               "Amount": float(row[29]),
               "Class": int(row[30]),
               "Feedback": feedback
           }
            message_id = publish_avro_record(record)
            print(f"Published message with ID: {message_id} (n={i})")


# Process all CSV files in the folder
blobs = storage_client.list_blobs(bucket, prefix=csv_folder_path)
for i, blob in enumerate(blobs):
    print(blob)
    if blob.name.endswith('.csv'):
        process_csv_blob(blob)
