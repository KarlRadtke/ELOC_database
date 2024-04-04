import io
import boto3
import warnings
import librosa
import pandas as pd
import yaml



def create_s3_client(config_path='config/connection_config.yaml'):
    '''
    Creates and returns an S3 client using credentials stored in a YAML configuration file.

    Args:
        config_path (str): Path to the YAML file containing the AWS credentials.

    Returns:
        boto3.Session.client: An S3 client configured with the specified credentials.
    '''
    # Load the S3 credentials from a YAML file
    try:
        with open(config_path, 'r') as f:
            credentials = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading the config file: {e}")
        return None
    
    # Extract the access key and secret access key
    access_key = credentials.get('access_key')
    secret_access_key = credentials.get('secret_access_key')

    if not access_key or not secret_access_key:
        print("Access key or secret access key not found in the configuration file.")
        return None
    
    # Connect to S3
    try:
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
        return s3
    except Exception as e:
        print(f"Error creating the S3 client: {e}")
        return None



def download_s3_object_to_memory(bucket_name: str, object_key: str, client: boto3.client) -> io.BytesIO:
    """
    Downloads an object from an S3 bucket and returns its contents as a BytesIO object.

    Parameters:
    bucket_name (str): The name of the S3 bucket.
    object_key (str): The key of the S3 object to download.
    client (boto3.client): The S3 client to be used for the download.

    Returns:
    io.BytesIO: The contents of the S3 object as a BytesIO object.

    Raises:
    UserWarning: If the object cannot be downloaded from the bucket.
    """
    try:
        object_bytes = io.BytesIO()
        response = client.get_object(Bucket=bucket_name, Key=object_key)
        object_bytes.write(response['Body'].read())
        object_bytes.seek(0)
        return object_bytes
    except Exception as e:
        warning_message = f"Failed to download S3 object: {object_key} from {bucket_name}. Exception message: {e}"
        warnings.warn(warning_message)
        return None


def read_audio_fromS3(audio_file_path, bucket_name, client):
    """
    Processes the audio file specified in the given row:
    1) downloading
    2) loading the audio data

    Parameters:
    row (pandas.Series): The row containing the information about the audio file.

    Returns:
    tuple or None: A tuple containing the loaded audio data and the sampling rate (audio_data, sr) if successful, or None if there was an error.

    Raises:
    UserWarning: If the audio file cannot be downloaded or loaded.
    """

    audio_bytes = download_s3_object_to_memory(bucket_name, audio_file_path, client)

    if audio_bytes is None:
        warning_message = f"Failed to download S3 object: {audio_file_path}."
        warnings.warn(warning_message)
        return None

    try:
        audio_data, sr = librosa.load(audio_bytes, sr=None)
        return audio_data, sr
    except Exception as e:
        warning_message = f"Failed to load audio: {audio_file_path}. Exception message: {e}"
        warnings.warn(warning_message)
        return None
    
       
    
def read_selection_table_fromS3(selection_table_path, bucket_name, client):
    """
    Processes the selection table specified in the given row:
    1) downloading
    2) loading it into a DataFrame
    Parameters:
    row (pandas.Series): The row containing the information about the selection table.
    
    Returns:
    pandas.DataFrame or None: The loaded selection table as a DataFrame if successful, or None if there was an error.
    
    Raises:
    UserWarning: If the selection table cannot be downloaded or loaded.
    """
    
    selection_table_bytes = download_s3_object_to_memory(bucket_name, selection_table_path, client)

    if selection_table_bytes is None:
        warning_message = f"Failed to download S3 object: {selection_table_path}."
        warnings.warn(warning_message)
        return None

    try:
        selection_table = pd.read_csv(selection_table_bytes, sep='\t')
        return selection_table
    except Exception as e:
        warning_message = f"Failed to load selection table: {selection_table_path}. Exception message: {e}"
        warnings.warn(warning_message)
        return None    
    
    

    
    
    
    
# Define a function to trim audio file
