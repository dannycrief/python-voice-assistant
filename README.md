# Mark Voice Assistant

- Mark Voice Assistant is a Python voice assistant project on SpeechRecognition, pyttsx3 and GoogleAPI
- At the moment Mark knows to read data from your Google Calendar (from first running you'll be redirected to Google login page)
and write data to file .txt using notepad.exe

## Installation
- clone project
- create virtual environments in the root of project and activate it:
- Windows:
```bash
pip install virtualenv
virtualenv myvenv_name
myvenv_name\Scripts\activate
```
- Linux:
```bash
sudo apt-get install python-pip
pip install virtualenv
virtualenv virtualenv_name
source virtualenv_name/bin/activate
```
- To make Mark Voice Assistant work correctly you'll be need to PyAudio library
- check you python version
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

## Usage
While you activate your virtual environments, you'll need to run it by typing in terminal from project root
```bash
python main.py
```
- Use "hey Mark" to wake Mark.
-Key phrases:
 1. "what do i have...", "do i have plans...", "am i busy.."
 2. "make a note", "write this down", "remember this"
## Examples using
- Hey Mark what do I have on Monday 2nd
- Hey Mark make a note
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
