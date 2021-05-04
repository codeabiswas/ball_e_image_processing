# Image Processing for Ball-E

This repository contains all the code and related files pertaining to image-processing related aspects for the Bi-Axial Autonomous Lacrosse Learning Evaluator (Ball-E).

## Pre-requisites
* `Python 3.6.9`
* `NumPy`
* `OpenCV`

## Branch Structure

### main
Contains 'production-level', 100% working code

### develop
Contains beta code. This will be the primary branch for system-wide testing

### feature branches
Feature branches are development branches which is always updated with the latest `develop` branch's code. A feature branch uses the following naming convention:

`feature/<ticket-#>`

## Project Structure

### src/
Contains code, usually `.py` files.

### src/focal\_length\_finder
Code for finding the focal length of the camera

## File Structure

All `.py` files are fomatted using `autopep8` and use `UTF-8` encoding.

## Acknowledgements and Usage Agreement
This code is written for the P21390 Project for Rochester Institute of Technology's, Kate Gleason College of Engineering's, Multidisciplinary Senior Design class. You may use and edit the contents of this code freely in your own projects as long as the following is mentioned in your source code/documentation at least once:
* This [Confluence page's URL](https://wiki.rit.edu/display/MSDShowcase/P21390+Bi-Axial+Autonomous+Lacrosse+Learning+Evaluator) which talks about the project

