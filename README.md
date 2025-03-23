# 🖥️ Desktop Assistant

![forks](https://img.shields.io/github/forks/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Watchers](https://img.shields.io/github/watchers/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Repo stars](https://img.shields.io/github/stars/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Contributors](https://img.shields.io/github/contributors/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)
![Issues](https://img.shields.io/github/issues/vihar-s1/Desktop-Assistant?style=for-the-badge&color=dark-green)

<!-- ![Project Logo](logo.png) -->

A simple Python-based desktop assistant that can perform basic tasks like searching on Google, opening applications, telling the time, and more WITHOUT the use of Machine Learning (ML) or Artificial Intelligence (AI).

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

- The project is a simple Python-based desktop assistant that can perform basic tasks like searching on Google, opening applications, telling the time, and more.
- The assistant is always under the development phase waiting for more features to be added.
- It is built using Python and does not use any Machine Learning (ML) or Artificial Intelligence (AI) models.
- The assistant is built using the `pyttsx3` library for text-to-speech conversion and the `speech_recognition` library for speech recognition.
- The project is open-source and contributions and/or feature requests are always welcome.

## 🚀 Getting Started

To get started with the project, follow the instructions below.

- The project is built using Python, so make sure you have Python installed on your system.

### 🛠️ Installation

1. Download and extract the zip file or clone the repository using the following command.

    ```bash
    git clone https://github.com/vihar-s1/Desktop-Assistant
    ```

2. In the project root directory run `setupProject.sh` script to create a virtual environment, and setup the project.

    ```bash
    bash setupProject.sh
    ```

3. Once setup is complete, simply run the `assistant.py` file to start using the Assistant.

    ```bash
    python3 assistant.py
    ```

### 🛠️ macOS Specific Fixes

If you encounter the following error on macOS:

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
  here: [Contributing Guidelines](CONTRIBUTING.md).
  
## 🐞 Bug Reports and Feature Requests

- If you encounter an issue or want to report a bug, following is
  the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.yml)
  you will be asked to follow.
- Any new feature requests will also be appreciated if it follows the predefined [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.yml).

> **NOTE:** The templates are predefined and integrated in the repository so you can go to
> the [Issues Tab](https://github.com/vihar-s1/Desktop-Assistant/issues) and start writing your bug report, or feature
> request without any problem.

## 💬 Discussion Groups

To discuss the project in depth with the contributors of the project about new features, bug requests, or just
suggestions, go to the [Discussion Page](https://github.com/vihar-s1/Desktop-Assistant/discussions) of the repository.
