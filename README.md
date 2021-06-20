# Sarah Voice Assistant
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/dannycrief/python-voice-assistant)
![GitHub issues](https://img.shields.io/github/issues/dannycrief/python-voice-assistant)
![GitHub last commit](https://img.shields.io/github/last-commit/dannycrief/python-voice-assistant)
- Sarah Voice Assistant is a Python voice assistant project on SpeechRecognition, pyttsx3 and GoogleAPI
- Sarah knows to read data from your Google Calendar (from first running you'll be redirected to Google login page),
read email from your Gmail, open browsers, write data to file .txt using notepad.exe and many interesning things 😉

## Installation
- Clone project
- Create virtual environments in the root of project and activate it:
- Windows:
```bash
pip install virtualenv
virtualenv myvenv_name
myvenv_name\Scripts\activate
```
- Linux: at this moment does not support on Linux and macOS

- To make Sarah Voice Assistant work correctly you'll be need to PyAudio library
- Check you python version
```bash
python --version
```
For example if your python version is 3.9 and 64 bit you'll be need PyAudio-0.2.11-<b>cp39</b>-cp39-<b>win_amd64</b> (just install from requirements.txt)
If it's different from Python 3.9 then download from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it:
```bash
pip install PyAudio-0.2.11-cp<python version>-cp<python version>-win<64 or 32 bit>.whl
```
- Install other requirements form requirements.txt
```bash
pip install -r requirements.txt
```
## Configuring Google Calendar API

- Use this [link](https://developers.google.com/calendar/quickstart/python) to enable the Google Calendar Api
- Click the button "Enable the Google Calendar API"
- Next step after downloading credentials.json put this file in project root
- On first running you'll need to accept Google privacy. (Even if browser will show you warning)

## Configuring Google  Gmail API

- Use this [link](https://developers.google.com/gmail/api/quickstart/python) to enable the Google Calendar Api
- Click the button "Enable the Google Calendar API"
- Next step after downloading credentials.json put this file in project root
- On first running you'll need to accept Google privacy. (Even if browser will show you warning)

### Usage
While you activate your virtual environments, you'll need to run it by typing in terminal from project root
```bash
python main.py
```

- Use "Hi Sarah" to wake Sarah. -Key phrases:

1. "what do I have...", "do I have plans...", "am I busy..."
2. "make a note", "write this down", "remember this"
3. "do I have new messages", "do I have messages"
4. "how can I get", "create a road", "create road", "how long do I need to ride"
5. "open browser"
## Examples using

- Hi Sarah what do I have on Monday 2nd
- Hi Sarah make a note
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
