#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
External Interface
===============

This module contains the paths of external applications and websites that are
used by the assistant. It also contains the features that the assistant can
perform.

"""

AppPath = {
    "microsoft word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "one note": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
    "1 note": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
    "chrome": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    "vs code": "C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "moodle": "C:\\Users\\HP\\AppData\\Local\\Programs\\moodledesktop\\Moodle Desktop.exe",
}


WebPath = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "coursera": "https://www.coursera.org",
    "leetcode": "https://leetcode.com",
    "gmail": "https://mail.google.com",
    "classroom": "https://classroom.google.com",
    "drive": "https://drive.google.com",
    "geeks for geeks": "https://geeksforgeeks.org",
}


features = {
    "search your query in google and return upto 10 results",
    "get a wikipedia search summary of upto 3 sentences",
    "open a certain preset applications or websites as per request",
    "tell you the time of the day",
}
