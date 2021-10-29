# E-Shelter_ObjectCount
 Detects and counts Object in Images. Running Python3 and OpenCV on Jupyter Nodebook
 This is no Yolo or object models based solution.  
 Im using matchTemplate from Open-CV on static images. 
 
 ![grafik](https://user-images.githubusercontent.com/12233951/139504264-8e635343-ed51-4efa-886c-429fc446c862.png)
 

## Why

- sometime you have to count hundrets of objects like in PDF CAD Files where you dont have access to the original files from the architect.
- You need y,x Coordinates of Objects in an Image

![grafik](https://user-images.githubusercontent.com/12233951/139503590-181669ac-5071-46e0-b2b8-8b23e4d56f2b.png)


![grafik](https://user-images.githubusercontent.com/12233951/139502750-384c77c2-411f-4e08-862a-5d3da3408d10.png)

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

### Workflow:
- Prepare your Haystack Image. Transparent Images are not working. Put it in the stacks Folder.
- Some Autocad Export PDFs are transparent. Add a white Background.
- Create a needle Image what you are looking for. The needle Image must have to same size as the objects you are looking for in the image. Copy it in the Needle Folder and rename it to needle_4k.png

Should look like this for the expample shown here:  ![grafik](https://github.com/corgan2222/E-Shelter_ObjectCount/blob/main/Jupyter/data/needle/needle_4k.png)


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
git clone https://github.com/corgan2222/E-Shelter_ObjectCount.git
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

then open the Jupyter URL in the Browser. Typically http://localhost:8888/lab?

## Settings

There are some setting you can adjust

- toggle Debug Information
- Adjust the Threshold for detection


# More Infos about

- https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html



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
- https://github.com/starcraft04/swauto ! Most of the code to prevent OpenCV from double counting. Thanks a lot! 
