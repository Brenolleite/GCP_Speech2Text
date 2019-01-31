## Google Cloud Speech to Text


## Instalation

- Create a Google Cloud Account
- Enable Speech API
- Create a Storage Bucket
- Create a API credential, using Services Account Key -> Generate JSON file
- Go to project file
- Run ```pip install -r requirements.txt``` 
- Be happy

## Usage

- Run ```python main.py [args]```
- Run ```python main.py -h``` for help

# args

- ```-f``` = File path to the audio to be transcribed
- ```-b``` = Bucket name
- ```-c``` = Path to credential file - JSON
- ```-s``` = To save to a file, if not set transcription will be printed on screen

# example

```python main.py -f audio.mp3 -b test -c test_credential.JSON -s```