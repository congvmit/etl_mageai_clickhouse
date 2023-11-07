from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from pandas import DataFrame
from os import path
import json


from minio import Minio
from minio.error import S3Error
from io import BytesIO

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> None:
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "localhost:9009",
        access_key="minio",
        secret_key="minio-password",
        secure=False
    )

    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists("dwh-staging")
    if not found:
        client.make_bucket("dwh-staging")
    else:
        print("Bucket 'dwh-staging' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    # client.fput_object(
    #     "asiatrip", "asiaphotos-2015.zip", "/home/user/Photos/asiaphotos.zip",
    # )
    # print(df)

    # csv_bytes = df.to_csv().encode('utf-8')
    csv_bytes = json.dumps(df, indent=2).encode('utf-8')
    # csv_bytes = df.encode('utf-8')
    csv_buffer = BytesIO(csv_bytes)

    client.put_object('dwh-staging',
                      'mypath/test.json',
                       data=csv_buffer,
                       length=len(csv_bytes),
                       content_type='application/json')
