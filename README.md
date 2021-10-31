# E-Shelter_ObjectCount

 Detects and counts Object in Images. Running Python3 and OpenCV on Jupyter Nodebook
 This is no Yolo or object models based solution.  
 Im using matchTemplate from Open-CV on static images.

 ![grafik](https://user-images.githubusercontent.com/12233951/139504264-8e635343-ed51-4efa-886c-429fc446c862.png)

<br>

## Why

- sometime you have to count hundrets of objects like in PDF CAD Files where you dont have access to the original files from the architect.
- You need y,x Coordinates of Objects in an Image

<br>

![grafik](https://user-images.githubusercontent.com/12233951/139503590-181669ac-5071-46e0-b2b8-8b23e4d56f2b.png)

![grafik](https://user-images.githubusercontent.com/12233951/139502750-384c77c2-411f-4e08-862a-5d3da3408d10.png)

<br>

## Features

- detect Objects in Images
- Count the objects
- Draw a rectangle and number on the object and save the image
- export the x,y coordinates to json, csv and text
- mass import for as many "haystack" images as you like
- Cross platform [Win,Linux] (no Idea about Mac)
- Windows executable

<br>

## Folder Structure

- Data<br>
   \  stacks         -   Insert the "haystack" Images here <br>
    \ needle         -   The "Needle" we want to find in the Haystack<br>
    \ output         -   Storage Folder for the processed Images<br>
    \ output_csv     -   Log Folder for txt,json and csv files<br>

<br>

## Informations

### Workflow

- Prepare your Haystack Image. Transparent Images are not working. Put it in the stacks Folder.
- Some Autocad Export PDFs are transparent. Add a white Background.
- Create a needle Image what you are looking for. The needle Image must have to same size as the objects you are looking for in the image. Copy it in the Needle Folder and rename it to needle_4k.png

Should look like this for the expample shown here:  ![grafik](https://github.com/corgan2222/E-Shelter_ObjectCount/blob/main/Jupyter/data/needle/needle_4k.png)

Haystack Images should be larger then the needle Images. I used around 4k resolution.
Put as many images as you like in the stacks Folder.
Importand is, that the needle Image has to be in the same size because the script don't resize the needle.

Look at the demo Image for an example.
If something goes wrong, set __DEBUG = True
<br>

# Windows executable

- Download latest Release Version from https://github.com/corgan2222/E-Shelter_ObjectCount/releases/ 
- Extract Zip File
- Start exe

# Source Installation Linux

```shell
git clone https://github.com/corgan2222/E-Shelter_ObjectCount.git
cd E-Shelter_ObjectCount/objectcounter
./install_linux.sh
python3 -m pip install -r requirements.txt 
```
<br>

# Source Installation Windows 

- Install WSL2 (Windows Subsystem for Linux)
- Install a Linux Distro like Ubuntu
- Login via SSH to your local WSL Instance

```shell
git clone https://github.com/corgan2222/E-Shelter_ObjectCount.git
cd E-Shelter_ObjectCount
chmod +x install.sh
./install_jupyter.sh

```

then open the Jupyter URL in the Browser. Typically <http://localhost:8888/lab>?
<br><br>

# Usage

There are two running modes.

## 1. Folder Based

```shell
python3 objectcounter.py
```

- just run the script with no parameter.
- The script will look in the data/stacks and data/needle Folder for Files.
- If the Output Folder not exists in the data Folder they got created

<br>

## 2. File based

<br>You can define all files and Folder via command line parameter

```shell
python3 objectcounter.py -i [image] -t [templatefile]
```

example Windows

```powershell
python3 objectcounter.py -i "c:\tmp\image.png" -t "c:\tmp\needle.png"
```

example Linux

```shell
python3 objectcounter.py -i "/home/user/files/image.png" -t "/home/user/files/needle.png"
```
<br>
<br>

# Command line Settings

| Option | Description | Notes |
| --- | ----------- | ---------- |
| -i | Imagefile | "/home/user/files/image.png"
| -t | Templatefile | "/home/user/files/needle.png"
| -o | Output Folder | "/home/user/files/data/output"
| -c | CSV&Txt Folder | "/home/user/files/data/output_csv"
| -s | Stacks Folder | "/home/user/files/data/stacks"
| -T | Tolerance | float 0-1 default 0.6
| -l | Logfile | "/car/log/debug.log"
| -v | verbose | show debug logs if set
| -q | quit | no output


<br>
<br>

# More Infos about

- <https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html>

<br>
<br>

## ToDo

- Testing, this is a alpha release
- add Screenshot Tool to create needle Images faster
- add flask Webserver
- Create Docker File
- make a standalone version for Windows user

<br>
<br>

## Thanks to

- Jupyter
- OpenCV
- <https://github.com/ClarityCoders>
- <https://github.com/starcraft04/swauto> ! Most of the code to prevent OpenCV from double counting. Thanks a lot!
