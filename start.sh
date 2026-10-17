#!/bin/bash

launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/local.create-lecture-notes.plist
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/local.load-slides-from-cloud.plist

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/local.create-lecture-notes.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/local.load-slides-from-cloud.plist

