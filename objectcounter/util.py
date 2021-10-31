import cv2 as cv2
import numpy as np
import os

def getCoordinates(top_left, w, h, best_val):
    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = (top_left[0] + (w/2), top_left[1] + (h/2))
    return [
        {
            'top_left': top_left,
            'bottom_right': bottom_right,
            'center': center,
            'tolerance': best_val,
        }
    ]


def extractAlpha(img, hardedge = True):
    if img.shape[2] <= 3:
        return {'res':False,'image':img}
    print('Mask detected')
    channels = cv2.split(img)
    mask = np.array(channels[3])
    if hardedge:
        for idx in xrange(len(mask[0])):
            mask[0][idx] = 0 if mask[0][idx] <=128 else 255
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    return {'res':True,'image':img,'mask':mask}


    
def twoSquaresDoOverlap(squareA,squareB):
    #The two squares must have coordinates in the form of named list with name top_left and bottom_right
    overlap = True
    if squareA['top_left'][1] > squareB['bottom_right'][1] or \
            squareA['top_left'][0] > squareB['bottom_right'][0] or \
            squareA['bottom_right'][0] < squareB['top_left'][0] or \
            squareA['bottom_right'][1] < squareB['top_left'][1]:
        overlap = False
            
    return overlap

def cropToCoords(img, coords):
    (ulx,uly) = coords[0]
    (brx,bry) = coords[1]
    return img[uly:bry, ulx:brx]



def getMultiFullInfo(all_matches,w,h):
    #This function will rearrange the data and calculate the tuple
    #   for the square and the center and the tolerance for each point
    result = []
    for match in all_matches:
        tlx = match[0]
        tly = match[1]
        top_left = (tlx,tly)
        brx = match[0] + w
        bry = match[1] + h 
        bottom_right = (brx,bry)     
        centerx = match[0] + w/2
        centery = match[1] + h/2
        center = [centerx,centery]
        result.append({'top_left':top_left,'bottom_right':bottom_right,'center':center,'tolerance':match[2]})
    return result    


def find_min_max(all_squares,axe,minormax):
    coord = 0 if axe == 'x' else 1
    best_result = {'res': all_squares['res'], 'points': []}
    best_result['points'].append(all_squares['points'][0])
    best_result['name'] = all_squares['name']

    for point in all_squares['points']:
        if minormax == 'max':
            if point['center'][coord] > best_result['points'][0]['center'][coord]:
                best_result['points'][0] = point
        elif point['center'][coord] < best_result['points'][0]['center'][coord]:
            best_result['points'][0] = point

    return best_result

def findAllPictureFiles(base_filename,directory):
    onlyfiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return [
        myfile
        for myfile in onlyfiles
        if myfile.startswith(base_filename)
        and not myfile[len(base_filename) :].startswith('_')
    ]

def fromStringToTuple(string):
    string = string.replace(' ', '')
    string = string.replace('(', '')
    string = string.replace(')', '')
    string = string.split(',')
    return int(string[0]), int(string[1])

def dictStringToInt(d):
    for key, value in d.iteritems():
        try:
            d[key] = int(value)
        except ValueError:
            d[key] = str(value)
    return d
