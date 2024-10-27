# 🖥️ Desktop Assistant

![forks](https://img.shields.io/github/forks/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Watchers](https://img.shields.io/github/watchers/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Repo stars](https://img.shields.io/github/stars/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Contributors](https://img.shields.io/github/contributors/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Issues](https://img.shields.io/github/issues/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)

<!-- ![Project Logo](logo.png) -->

A simple voice-assisted desktop assistant made in Python. The assistant will have basic features supporting daily laptop usage.

## Table of Contents

- [🖥️ Desktop Assistant](#-desktop-assistant)
  - [Table of Contents](#table-of-contents)
  - [🚀 Introduction](#-introduction)
  - [✨ Features](#-features)
  - [🚀 Getting Started](#-getting-started)
    - [📋 Prerequisites](#-prerequisites)
    - [🛠️ Installation](#-installation)
  - [🤝 Contributing](#-contributing)
  - [🐞 Bug Reports and Feature Requests](#-bug-reports-and-feature-requests)
  - [💬 Discussion Groups](#-discussion-groups)

## 🚀 Introduction

- A Python-based desktop assistant configured to automate some of the day-to-day tasks and help save time.
- Voice assistance is used to provide a hands-free interface to the user as the assistant can run in the background while performing day-to-day tasks.
- `external_paths.py` and `support.py` files are for having additional globally required variables, and query functions
  handling individual queries respectively.
- The `voice_interface.py` file contains the **_VoiceInterface_** class which handles the abstraction of user voice
  recognition and assistant speech.
- The `assistant.py` file contains the main code integrating everything together to run the assistant properly.

## ✨ Features

- Google and Wikipedia searches 🌐
- Run applications or websites from a predefined map/list 🚀
- Tell time of the day in _hour **:** minute **:** second_ format ⏰

## 🚀 Getting Started

- Fork or download the project.
- Install the Python dependencies mentioned in the `requirements.txt` file using pip or pip3.
- Run the main Python file named `assistant.py` in the project root folder to run the assistant.

### 📋 Prerequisites

- The project is coded using `Python 3.11.0`, so it would be best to install an equivalent or later version.
- The modules required are listed in the requirements.txt file which can be installed as discussed below.

### 🛠️ Installation

1. Download and extract the zip file or clone the repository using the following command.

    ```bash
    git clone https://github.com/vihar-s1/Desktop-Assistant
    ```

2. In the project root directory run following script to create a virtual environment, and setup the project.

    ```bash
    bash setupProject.sh
    ```

3. Once setup is complete, simply run the `assistant.py` file to start using the Assistant.

    ```bash
    python assistant.py
    ```

### 🛠️ macOS Specific Fixes

If you encounter the following error on MacOS:

#### @objc.python_method annotation error

> File ".../.venv/lib/python3.12/site-packages/pyttsx3/drivers/nsss.py", line 27, in NSSpeechDriver  
>    @objc.python_method  
>    ^^^^  
> NameError: name 'objc' is not defined. Did you mean: 'object'?  

Then open the `nsss.py` library file and import `objc` at the top of the file.

```python
import objc
```

You may need to install `PyObjC` using the following command:

```bash
pip3 install pyobjc
```

#### NSSpeechDriver super() error

If you encounter the following error:

>   File "/Users/viharshah/Desktop/IdeaProjects/Desktop-Assistant/.venv/lib/python3.12/site-packages/pyttsx3/drivers/nsss.py", line 30, in initWithProxy  
> self = super(NSSpeechDriver, self).init()  
> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
> AttributeError: 'super' object has no attribute 'init'  
> sys:1: UninitializedDeallocWarning: leaking an uninitialized object of type NSSpeechDriver

Then replace the `super(NSSpeechDriver, self).init()` line with the following:

```python3
objc.super(NSSpeechDriver, self).init()
```

## 🤝 Contributing

- If you want to contribute, follow the contribution guidelines
  here: [Contributing Guidelines](https://github.com/vihar-s1/Desktop-Assistant/blob/main/CONTRIBUTING.md).

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```
  
- Make Sure to update the `requirements.txt` file by adding to it appropriate required packages and corresponding versions.

## 🐞 Bug Reports and Feature Requests

- If you encounter an issue or want to report a bug, following is
  the [Bug Report Template](https://github.com/vihar-s1/Desktop-Assistant/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)
  you will be asked to follow.
- Any new feature requests will also be appreciated if it follows the predefined [Feature Request Template](https://github.com/vihar-s1/Desktop-Assistant/blob/main/.github/ISSUE_TEMPLATE/feature_request.md).

> **NOTE:** The templates are predefined and integrated in the repository so you can go to
> the [Issues Tab](https://github.com/vihar-s1/Desktop-Assistant/issues) and start writing your bug report, or feature
> request without any problem.

## 💬 Discussion Groups

To discuss the project in depth with the contributors of the project about new features, bug requests, or just
suggestions, go to the [Discussion Page](https://github.com/vihar-s1/Desktop-Assistant/discussions) of the repository.
