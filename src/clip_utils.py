import os
import io
import soundfile as sf
import librosa
from .s3_utils import read_audio_fromS3, read_selection_table_fromS3



def trim_audio_file(audio_data, onset_time, offset_time, sr):
    """
    Trims an audio data array based on the given onset and offset times.

    Parameters:
    audio_data (numpy.ndarray): The audio data to be trimmed.
    onset_time (float): The onset time in seconds.
    offset_time (float): The offset time in seconds.
    sr (int): The sampling rate of the audio data.

    Returns:
    numpy.ndarray: The trimmed audio data array.

    Raises:
    None
    """
    onset_sample = librosa.time_to_samples(onset_time, sr=sr)
    offset_sample = librosa.time_to_samples(offset_time, sr=sr)
    return audio_data[onset_sample:offset_sample]




def extract_and_upload_clips(
    soundfile_directory, selection_table_directory, 
    bucket_name, client
    ):
    
    """
    extracts clips containing elephants from soundfile
    uploads clips to the respective bucket
    
    Parameters:
    - soundfile_path (str): S3 path to the source audio file.
    - selection_table_path (str): S3 path to the selection table CSV.
    - bucket (str): Name of the S3 bucket.
    - s3_client: Instance of the S3 client.
    """
    
    
    audio, sr = read_audio_fromS3(soundfile_directory, bucket_name, client)
    selection_table = read_selection_table_fromS3(selection_table_directory, bucket_name, client)
    
    for _, label in selection_table.iterrows():
        # gather informations from selection table
        start, end = label["Begin Time (s)"], label["End Time (s)"]
        sound_category = label['sound_category']
        sound_type = label['sound_type']
        label_id = label["label_id"]
        confidence = str(label["confidence"])
        # create file- and foldernames
        output_dir = f"soundfiles_trimmed/confidence_{confidence}/{sound_category}/{sound_type}/"
        filename = f"{label_id}.wav"
        output_path = os.path.join(output_dir, filename)
        
        # extract clip
        clip = trim_audio_file(audio, start, end, sr)
        
        # upload to S3
        with io.BytesIO() as audio_file:
            sf.write(audio_file, clip, sr, format='WAV', subtype='PCM_16')
            audio_file.seek(0)
            client.upload_fileobj(
                audio_file, 
                bucket_name, 
                output_path, 
                ExtraArgs={'ContentType': 'audio/wav'}
            )