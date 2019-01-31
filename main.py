import os
import argparse
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage
import librosa
import subprocess

def upload(file_path, bucket_name):
    # Open client with Credentials for Storage API
    storage_client = storage.Client()
    
    # Select bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Create and upload file
    blob = bucket.blob(file_path.split('/')[-1])
    blob.upload_from_filename('NEW_' + file_path)

    # Removing file from computer    
    os.remove('NEW_' + file_path)

    return blob

def transcribe(file_path, bucket_name, sample_rate, duration):
    # Open client with credentials for Speech to Text API
    client = speech.SpeechClient()

    # Configure audio to transcribe in GCP
    audio = types.RecognitionAudio(uri='gs://' + bucket_name + '/' + file_path.split('/')[-1])
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,   
        sample_rate_hertz = sample_rate,
        language_code='pt-BR')

    # Create operation to transcribe
    operation = client.long_running_recognize(config, audio)

    # Wait on async call to transcribe
    print('\n\n\n=====================================================================================\n' +
          'Executando transcrição, a mesma costuma levar cerca de 1/2 do tempo total do áudio' +
          '\n=====================================================================================\n\n\n')
    response = operation.result(timeout = duration)
    
    # Create a list with transcription
    text = []
    for result in response.results:
        text.append((result.alternatives[0].transcript))
    
    return text

def config_audio(file_path):
    # Get audio sample rate
    signal, sample_rate = librosa.load(file_path, sr = None)

    # Get duration
    duration = int(librosa.get_duration(signal, sample_rate))

    # Replace any ext to .wav
    new_path = file_path.replace(file_path.split('.')[-1].split('.')[-1], 'wav')

    # Save audio as mono channel and wav - PCM    
    subprocess.call(['ffmpeg', '-i', file_path, '-acodec', 'pcm_s16le', '-ar', str(sample_rate), 
                     '-ac', str(1), 'NEW_' + new_path, '-hide_banner', '-loglevel', '0'])

    return new_path, sample_rate, duration

if (__name__ == '__main__'): 
    # Create argument parser 
    ap = argparse.ArgumentParser(description='Google Transcription')

    ap.add_argument('-f', '--file_path',
                    dest='file_path',
                    help='Caminho para o arquivo a ser transcrito.',
                    type=str,
                    required=True)

    ap.add_argument('-b', '--bucket_name',
                    dest='bucket_name',
                    help='Nome do Bucket no Google Cloud.',
                    type=str,
                    required=True)

    ap.add_argument('-c', '--credential_file_path',
                    dest='credential_file_path',
                    help='Caminho para o arquivo JSON de credencial criado pela Google Cloud.',
                    type=str,
                    required=True)

    ap.add_argument('-s', '--save',
                    dest='save',
                    help='Criar um arquivo para salvar a transcrição.',
                    action='store_true')

    # Create variable with arguments
    ARGS = ap.parse_args()

    # Setting env variables for GCP credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ARGS.credential_file_path

    # Configure audio - Convert to wav and mono channel
    file_path, sample_rate, duration = config_audio(ARGS.file_path)

    # Upload to GCP for transcription
    blob = upload(file_path, ARGS.bucket_name)

    # Transcribe file - Use > to save results to file
    text = transcribe(file_path, ARGS.bucket_name, sample_rate, duration)

    # Joining text for all transcriptions
    text = ' '.join(text)

    # If save is set, create a file with file_path.txt
    if (ARGS.save):
        save_path = file_path.replace(file_path.split('.')[-1].split('.')[-1], 'txt')
        f = open(save_path, "w")
        f.write(text)
        f.close()
        print('OK - Arquivo salvo ->', save_path)
    else:
        print(text)

    # Removing file from GCP
    blob.delete()