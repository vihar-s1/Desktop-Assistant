# Desktop Assistant

![forks](https://img.shields.io/github/forks/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Watchers](https://img.shields.io/github/watchers/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Repo stars](https://img.shields.io/github/stars/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Contributors](https://img.shields.io/github/contributors/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Issues](https://img.shields.io/github/issues/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)

<!-- ![Project Logo](logo.png) -->

A simple voice-assisted desktop assistant made in python. The assistant will have the basic features supporting daily laptop usage.

## Table of Contents

- [Desktop Assistant](#desktop-assistant)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Contributing](#contributing)
  - [Bug Reports and Feature Requests](#bug-reports-and-feature-requests)

## Introduction

- A python based desktop assistant configured to automate of some of the day-to-day tasks and help person save some time.
- Voice assistance is used to provide a hands-free interface to the user as the assistant can run in the background while perform your day-to-day tasks.
- `Extras.py` and `Support.py` files are for having additional globally required variables, and query functions handling individual queries respectively.
- The  `VoiceInterface.py` file contains the **_VoiceInterface_** class which handles the abstraction of user voice recognition and assistant speech.
- The `Assistant.py` file contains the main code integrating everything together to run the assistant properly.

## Features

List the key features of your project. You can use bullet points for this section.

- Google and Wikipedia searches
- Run application or website from a predefined map/list
- Tell time of the day _hour **:** minute **:** sec_ format

## Getting Started

- Fork or download the project.
- Install the python dependancies mentioned in the `requirements.txt` file using pip or pip3.
- Run the main python file named `Assistant.py` in the project root folder to run the assistant.
  
### Prerequisites

- The project is coded using `python3.11.0`, so it would be best to install an equivalent or later version.
- The modules required are listed in the requirements.txt file which can be installed as discussed below.

### Installation

1. Download and extract the zip file or clone the repository using below command.

```bash
git clone https://github.com/vihar-s1/Desktop-Assistant
```

2. In the project root directory run following commands to create a virtual environment, activate it, and install the python module dependencies.

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

3. Once installed, simply run the `Assistant.py` file to start using the Assistant.

```bash
python Assistant.py
```

## Contributing

- If you want to contribute, follow the contribution guidelines here: [Contributing Guidelines](https://github.com/vihar-s1/Desktop-Assistant/blob/main/CONTRIBUTING.md)
  
- Create a virtual environment for contributing to prevent unnecessary packages from being included in the `requirements.txt` file while updating it via `updateRequirementsFile.sh`

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```
  
- Make Sure to update the `requirements.txt` file by running `updateRequirementsFile.sh` in case any additional packages are installed.

```bash
bash updateRequirementsFile.sh
```

## Bug Reports and Feature Requests

- If you encountered an issue or want to report a bug, following is the [Bug Report Template](https://github.com/vihar-s1/Desktop-Assistant/blob/main/.github/ISSUE_TEMPLATE/bug_report.md) you will be asked to follow.
- Any new feature requests will also appreciated if it follows the predefined [Feature Request Template](https://github.com/vihar-s1/Desktop-Assistant/blob/main/.github/ISSUE_TEMPLATE/feature_request.md).

> **NOTE:** The templates are predefined and integrated in the repository so you can easily go to the [Issues Tab](https://github.com/vihar-s1/Desktop-Assistant/issues) and start writing your bug report, or feature request without any problem.
