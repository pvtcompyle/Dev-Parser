@echo off
cls
rem Change this directory to the location of your devparse.py file
python R:\GitHub\Dev-Parser\devparse.py -p %1
timeout 30