import os
import csv
import json

def checkFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def saveTextFile(data, filename):           
    with open(filename,"w") as filewrite:
        filewrite.write(str(data))
   
def saveCSV(data, filename):        
    fieldnames = ['objectID', 'top_left_x', 'top_left_y',  'bottom_right_x', 'bottom_right_y',  'center_x', 'center_y', 'tolerance' ]
    with open(filename, mode='w') as csv_file:        
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fieldnames)              
        writer.writerows(data)
        
def saveJson(data, filename):        
    with open(filename, 'w') as outfile:
      json.dump(data, outfile, ensure_ascii=False)     


def checkInputFolderPath(giveFolder, defaultStr):
    if len(giveFolder) > 0 & os.path.exists(giveFolder):
        return giveFolder

    cwd = os.getcwd()
    folder = os.path.join(cwd, 'data',defaultStr)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder    
      