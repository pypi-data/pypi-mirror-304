import boto3
import os
import datetime
import zipfile
from fsd.log.logger_config import get_logger
import tempfile

logger = get_logger(__name__)

def upload_file_to_s3(file_path, bucket_name, s3_key):
    """
    Uploads a file to an S3 bucket.

    :param file_path: Path to the file to upload
    :param bucket_name: Name of the S3 bucket
    :param s3_key: S3 object key
    """
    try:
        s3 = boto3.client('s3')
        s3.upload_file(file_path, bucket_name, s3_key)
        logger.info(f"Successfully uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        logger.error(f"Failed to upload {file_path} to S3: {e}")
        raise

def deploy_zip_to_s3(local_directory):
    """
    Creates a zip file from a local directory and uploads it to S3.

    :param local_directory: Path to the local directory to be zipped and uploaded
    :return: S3 key of the uploaded zip file
    """
    bucket_name = 'zinley'
    s3_prefix = 'fsd/'
    ignore_files = ['.git', '.DS_Store', '.zinley', '.zinley.tags.cache.v3', '.gitignore']

    # Ensure the local_directory is an absolute path
    local_directory = os.path.abspath(local_directory)
    logger.debug(f"Local directory to zip: {local_directory}")

    # Create a temporary directory to store the zip file
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_web.zip"
        zip_filepath = os.path.join(temp_dir, zip_filename)
        logger.debug(f"Temporary zip file path: {zip_filepath}")

        # Create the zip file
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(local_directory, topdown=True):
                # Remove ignored directories from traversal
                dirs[:] = [d for d in dirs if d not in ignore_files]
                for file in files:
                    if file not in ignore_files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, local_directory)
                        if os.path.isfile(file_path):  # Ensure it's a file
                            zipf.write(file_path, arcname)
                            logger.debug(f"Added {file_path} as {arcname}")

        # Verify that the zip file is not empty
        if os.path.getsize(zip_filepath) == 0:
            logger.error(f"Generated zip file {zip_filepath} is empty. No files were added.")
            raise ValueError(f"Generated zip file {zip_filepath} is empty. No files were added.")

        # Generate the S3 key for the zip file
        s3_key = f"{s3_prefix}{os.path.basename(local_directory)}_{zip_filename}"
        logger.debug(f"S3 key for upload: {s3_key}")

        # Upload the zip file to S3
        upload_file_to_s3(zip_filepath, bucket_name, s3_key)

        # TemporaryDirectory context automatically cleans up the temp_dir
        logger.info(f"Deployment successful. Zip file uploaded to s3://{bucket_name}/{s3_key}")

        return s3_key
