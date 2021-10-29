# E-Shelter_ObjectCount
 Detects and counts Object in Images. Running OpenCV on Jupyter Nodebook

## Features

- detect Objects in Images
- Count the objects 
- Draw a rectangle and number on the object and save the image
- export the x,y coordinates to json, csv and text
- mass import for as many "haystack" images as you like


## Folder Structure:

- Data<br>
   \  stacks         -   Insert the "haystack" Images here <br>
    \ needle         -   The "Needle" we want to find in the Haystack<br>
    \ output         -   Storage Folder for the processed Images<br>
    \ output_csv     -   Log Folder for txt,json and csv files<br>
   
## Informations

Haystack Images should be larger then the needle Images. I used around 4k resolution.
Put as many images as you like in the stacks Folder.
Importand is, that the needle Image has to be in the same size because the script don't resize the needle.

Look at the demo Image for an example.
If something goes wrong, set __DEBUG = True

## Installation

Windows User:
- Install WSL2 (Windows Subsystem for Linux)
- Install a Linux Distro like Ubuntu
- Login via SSH to your local WSL Instance

```shell
# git clone https://github.com/corgan2222/E-Shelter_ObjectCount.git
cd E-Shelter_ObjectCount
chmod +x install.sh
./install.sh

```
The installer will install

```sudo apt install git python3 python3-pip pipenv
python3 -m pip install --user pipenv
pipenv install jupyterlab
pipenv shell
jupyter lab
```



## ToDo:

- Testing, this is a alpha release
- add Screenshot Tool to create needle Images faster
- add flask Webserver
- Create Docker File
- make a standalone version for Windows user

## Thanks to

- Jupyter
- OpenCV
- https://github.com/ClarityCoders 
- https://github.com/starcraft04/swauto 
