## Google Cloud Speech to Text


## Instalation

- Create a Google Cloud Account
- Enable Speech API
- Create a Storage Bucket
- Create a API credential, using Services Account Key -> Generate JSON file
- Go to project file
- Run ```pip install -r requirements.txt``` 
- Be happy...

## Usage

- Run ```python main.py [args]```
- Run ```python main.py -h``` for help

# args

- ```-f``` = File path to the audio to be transcribed
- ```-b``` = Bucket name
- ```-c``` = Path to credential file - JSON
- ```-s``` = To save to a file, if not set transcription will be printed on screen

# example

```python main.py -f my_audio.mp3 -b my_bucket_name -c my_credential.json -s```

# Tips

- Wav files tend to have better performance
- Run one audio per time, transcription of long files might be huge memory consuming. It will throw seg fault when memory is full.