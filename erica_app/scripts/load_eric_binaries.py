import boto3
from os import environ, remove, mkdir
import zipfile
import shutil

import click as click

BUCKET_NAME = environ.get("ERICA_BUCKET_NAME")
ERIC_BINARIES_NAME = "lib.zip"
ERIC_TARGET_FOLDER = "erica/lib"
ERICA_CERT_NAME = "cert.pfx"
ERICA_CERT_TARGET_DEST = "erica/instances/blueprint"
ENDPOINT_URL = environ.get("ENDPOINT_URL")


@click.group()
def cli():
    pass


def get_connected_session():
    # Get our session
    session = boto3.session.Session()
    s3 = session.resource(
        service_name='s3',
        endpoint_url=ENDPOINT_URL
    )
    return s3


def get_connected_client():
    s3 = get_connected_session()
    # Get our client
    return s3.meta.client


@cli.command()
@click.option('--bucket_name', help='Name of the bucket you want to create.')
def create_bucket(bucket_name, s3client=None):
    if not s3client:
        s3client = get_connected_client()

    s3client.create_bucket(Bucket=bucket_name)


@cli.command()
def list_buckets(s3client=None):
    if not s3client:
        s3client = get_connected_client()

    response = s3client.list_buckets()
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')


@cli.command()
@click.option('--bucket_name', help='Name of the bucket you want to upload the file to.')
@click.option('--object_name', help='Name of the object you want to store the file in.')
@click.option('--file_name', help='Name of the file you want to upload.')
def upload_file(bucket_name, object_name, file_name, s3client=None):
    if not s3client:
        s3client = get_connected_client()

    with open(file_name, "rb") as f:
        s3client.upload_fileobj(f, bucket_name, object_name)


@cli.command()
@click.option('--bucket_name', help='Name of the bucket you want to download the file from.')
@click.option('--object_name', help='Name of the object you want to download.')
@click.option('--file_name', help='Name of the file you want to store the downloaded object into.')
def download_file(bucket_name, object_name, file_name, s3client=None):
    if not s3client:
        s3client = get_connected_client()

    s3client.download_file(bucket_name, object_name, file_name)


@cli.command()
@click.option('--bucket_name', help='Name of the bucket you want to list of which you want to list the files.')
def list_objects_in_bucket(bucket):
    if isinstance(str, bucket):
        bucket = get_connected_session().Bucket(bucket)
    for bucket_object in bucket.objects.all():
        print(bucket_object)


@cli.command()
@click.pass_context
def download_eric_cert_and_binaries(ctx):
    s3client = get_connected_client()
    print("Downloading eric binaries")

    ctx.invoke(download_file, s3client=s3client, bucket_name=BUCKET_NAME,
               object_name=ERIC_BINARIES_NAME, file_name=ERIC_BINARIES_NAME)
    with zipfile.ZipFile(ERIC_BINARIES_NAME) as z:
        z.extractall(ERIC_TARGET_FOLDER)
        print("Extracted ERIC")
    remove(ERIC_BINARIES_NAME)

    print("Downloading cert")
    ctx.invoke(download_file, s3client=s3client, bucket_name=BUCKET_NAME,
               object_name=ERICA_CERT_NAME, file_name=ERICA_CERT_NAME)
    print("Moving cert")
    try:
        mkdir(ERICA_CERT_TARGET_DEST)
    except FileExistsError:
        print("Blueprint folder exists and does not need to be created")
    shutil.move(ERICA_CERT_NAME, ERICA_CERT_TARGET_DEST + "/" + ERICA_CERT_NAME)


if __name__ == "__main__":
    cli()
