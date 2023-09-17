# Desktop-Assistant

![GitHub forks](https://img.shields.io/github/forks/vihar-s1/Desktop-Assistant?style=for-the-badge)
[![Watchers](https://img.shields.io/github/watchers/vihar-s1/Desktop-Assistant?style=for-the-badge)](https://github.com/smv1999/pysh/watchers)

## Introduction

> A simple voice-assisted desktop assistant made in python.
> The assistant will have the basic features supporting daily laptop usage.

## Current Features

- Searching in google and returning results
- Returning a wikipedia search summary of 3 sentences
- Opening certain _applications/websites_ whose _filepath/url-links_ are located in `ExternalPath.py` as dictionary
- Tells the time of the day in **_hour:minute:seconds_** format

## File Structure

### `Requirements.txt`

- Contains list of additional python modules that may need to be installed separately.

### `Extras.py` and `Support.py`

- `Extras.py` contains additional variables defined for using throughout the Assistant.
- Currently, it contains the Application locations and Website URLs for certain specific applications and webistes to open through the assistant
- `Support.py` contains various functions used to assist in different tasks including query execution.

### `VoiceInterace.py`

- Contains a **VoiceInterface** class defination which consists of a voice engine and recognizer instance.
- The voice Engine is used to give voice to the assistant and can be configured to different predefined voices available in the user's system.
- The Voice Recognizer helps in converting user's speech to text by recording the audio and then processing it via google_recognizer.

### `Assistant.py`

- Contains the code for the Voice Assistant.
- Has functions to listen for query, execute a query (uses _if-elif-else_ blocks and _regex_ to analysis query), close assistant or reset/reinitiate assistant.
  