#!/bin/bash

wd=$PWD
#Setup google calendar tokens
cd g_calendar/
python quickstart.py
cp token.json $wd
cp $wd

python main.py