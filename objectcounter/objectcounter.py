#!/usr/bin/env python3

import os
import cv2 as cv2
import numpy as np
import argparse
import logging
import sys
import json
import export
import util
import logging
from rich.logging import RichHandler
from pathlib import Path

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DEFAULT_LOG_LEVEL = "INFO"


def getMulti(res, tolerance,w,h):
    #We get an opencv image in the form of a numpy array and we need to
    #   find all the occurances in there knowing that 2 squares cannot intersect
    #This will give us exactly the matches that are unique

    #First we need to get all the points where value is >= tolerance
    #This wil get sometimes some squares that vary only from some pixels and that are overlapping
    all_matches_full = np.where (res >= tolerance)

    #Now we need to arrange it in x,y coordinates
    all_matches_coords = [
        [pt[0], pt[1], res[pt[1]][pt[0]]]
        for pt in zip(*all_matches_full[::-1])
    ]

    #Let's sort the new array
    all_matches_coords = sorted(all_matches_coords)

    #This function will be called only when there is at least one match so if matchtemplate returns something
    #This means we have found at least one record so we can prepare the analysis and loop through each records 
    all_matches = [[all_matches_coords[0][0],all_matches_coords[0][1],all_matches_coords[0][2]]]
    for i, pt in enumerate(all_matches_coords, start=1):
        found_in_existing = False
        for match in all_matches:
            #This is the test to make sure that the square we analyse doesn't overlap with one of the squares already found
            if pt[0] >= (match[0]-w) and pt[0] <= (match[0]+w) and pt[1] >= (match[1]-h) and pt[1] <= (match[1]+h):
                found_in_existing = True
                if pt[2] > match[2]:
                    match[0] = pt[0]
                    match[1] = pt[1]
                    match[2] = res[pt[1]][pt[0]]
        if not found_in_existing:
            all_matches.append([pt[0],pt[1],res[pt[1]][pt[0]]])
    #Before returning the result, we will arrange it with data easily accessible
    all_matches = util.getMultiFullInfo(all_matches,w,h)
    return all_matches 

def findPicture(screenshot,template, tolerance, multiple = False ):
    #This function will work with color images 3 channels minimum
    #The template can have an alpha channel and we will extract it to have the mask
    
    log.info("[bold green]-Start of findPicture-[/]", extra={"markup": True})
    log.info('Tolerance to check is %f' , tolerance)

    h = template.shape[0]
    w = template.shape[1]

    #We will now extract the alpha channel
    tmpl = util.extractAlpha(template)
    #print('alpha')

    # the method used for comparison, can be ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    meth = 'cv2.TM_CCOEFF_NORMED'
    method = eval(meth)

    # Apply template Matching
    if tmpl['res']:
        res = cv2.matchTemplate(screenshot,tmpl['image'],method, mask = tmpl['mask'])
    else:
        res = cv2.matchTemplate(screenshot,tmpl['image'],method)

    #print('res')    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        best_val = 1 - min_val
    else:
        top_left = max_loc
        best_val = max_val
    #We need to ensure we found at least one match otherwise we return false    
    #print('*best_val; ' + str(best_val) + " , tolerance:" + str(tolerance))   

    if best_val >= tolerance:
        if multiple:
            #We need to find all the time the image is found
            all_matches = getMulti(res, float(tolerance),int(w),int(h))
        else:
            all_matches = util.getCoordinates(top_left, w, h, best_val)
        
        # log.debug('The points found will be:')
        # log.debug(all_matches)
        # log.debug('*************End of checkPicture')
            #return {'res': True,'best_val':best_val,'points':all_matches}                    
        return all_matches
    else:
        all_matches = util.getCoordinates(top_left, w, h, best_val)
        log.error('Could not find a value above tolerance')
        log.error('*************End of findPicture')
        return {'res': False,'best_val':best_val,'points':all_matches}

    

def runCounter(stackFile, needleFile, treshhold, output_path=""):  
    #Main Function

    if not os.path.exists(stackFile):
        log.error("[bold red blink]Stacks File found " + stackFile + " [/]", extra={"markup": True})  
        log.error("give valid Template File with option -i or put it in stacks Folder")  
        log.error("Exit")  

    if not os.path.exists(needleFile):
        log.error("[bold red blink]Template File found " + needleFile + " [/]", extra={"markup": True})  
        log.error("give valid Template File with option -t or put it in needle Folder")  
        log.error("Exit")  
        return 

    stack_file_name = os.path.basename(stackFile)     
    #read stackfile
    img_rgb = cv2.imread(stackFile)
    
    #grayImage
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    #needleFile
    template = cv2.imread(needleFile,1)
    
    #find matches
    matches = findPicture(img_rgb, template, treshhold, multiple = True)   
    
    count=0
    rows = []
    json_data = {'objects': [{'a':'1'}]}
    
    #main loop, itterates through each coordinate found   
    for resultp in matches:
        count +=1 
        
        #draw rectangle on stack image
        cv2.rectangle(img_rgb, resultp['top_left'], resultp['bottom_right'], (0,0,255), 2)   
        
        #add counter text on stack image
        cv2.putText(img_rgb, str(count), (resultp['top_left'][0] ,resultp['top_left'][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 1)  
        
        #log.debug(str(count) + ": " + str(resultp['top_left']))  
            
        #formating for csv   
        row = [count, resultp['top_left'][0], resultp['top_left'][1], resultp['bottom_right'][0], resultp['bottom_right'][1], resultp['center'][0], resultp['center'][1], resultp['tolerance'] ]        
        rows.append(row)

        #formating for json
        json_data['objects'].append( { "objectID": count , "top_left": [int(resultp['top_left'][0]),int(resultp['top_left'][1])], "bottom_right":[int(resultp['bottom_right'][0]),int(resultp['bottom_right'][1])], "center":[int(resultp['center'][0]),int(resultp['center'][1])], "tolerance": json.dumps(float(resultp['tolerance'])) } ) 
        
        
    #save to text    
    txt_output_path = os.path.join(csv_path,stack_file_name + '.txt')
    export.saveTextFile(matches, txt_output_path)   

    #save to csv
    csv_output_path = os.path.join(csv_path,stack_file_name + '.csv')
    export.saveCSV(rows, csv_output_path)

    #save json
    json_output_path = os.path.join(csv_path,stack_file_name + '.json')
    export.saveJson(json_data, json_output_path)
    
    #get x,y coordinates from stack image to print the counter text
    hi, wi, ci = img_rgb.shape   
    cv2.putText(img_rgb, "Count:" + str(count), (100, hi - 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)    

    #save processed images 
    output_path = os.path.join(output_path,stack_file_name + '_counter_.png')
    log.info("Save image to:" + output_path)    
    cv2.imwrite( output_path ,img_rgb)  

    #cv2.imshow(stackFile + '_counter_.png', img_rgb) #chrashed jupytier if count>1
    log.info("[bold green blink]- Finished! Found " + str(count) + " [/]", extra={"markup": True})
             

def allImagesMode(arg_tolerance):
    #Reads all images from Stack Folder                 
    for filename in os.listdir(stacks_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):        
            log.info("Process Stack file: " + os.path.join(stacks_path, filename))
            #run counter on each image with given needle
            #[path,needle,treshhold,debug]
            runCounter(os.path.join(stacks_path,filename),os.path.join(needle_path,'needle.png'),arg_tolerance,output_path)
        else:
            log.error("No Files found in:" + output_path)
            continue  

def is_valid_file(parser, arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg   

def get_parser():
    """Get parser object """
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = argparse.ArgumentParser(description='Understand functioning')
    parser.add_argument("-i", "--image", type=str, required=False,  metavar="FILE", help="Path to input image where we'll apply template matching", default="") 
    parser.add_argument("-t", "--template", type=str, required=False,  metavar="FILE", help="Path to template image", default="") 
    parser.add_argument("-o", "--outputfolder", type=str, required=False,  metavar="FILE", help="Path to output folder", default="") 
    parser.add_argument("-c", "--csvfolder", type=str, required=False,  metavar="FILE", help="Path to txt,csv folder", default="") 
    parser.add_argument("-s", "--stacksfolder", type=str, required=False,  metavar="FILE", help="Path to stacks folder", default="") 
    parser.add_argument("-T", "--tolerance", type=float, required=False, help="Tolerance to check value from 0-1", default=0.6)
    parser.add_argument("-l", "--logfile", type=str, required=False, help="Logfile", default="")
    parser.add_argument("--verbose", "-v", dest="log_level", action="append_const", const=-1,)
    parser.add_argument("--quiet", "-q", dest="log_level", action="append_const", const=1,)

    return parser

def setLogging(args):   
    log_level = LOG_LEVELS.index(DEFAULT_LOG_LEVEL)
    for adjustment in args.log_level or ():
            log_level = min(len(LOG_LEVELS) - 1, max(log_level + adjustment, 0))

    log_level_name = LOG_LEVELS[log_level]

    global log
    log = logging.getLogger(__name__)    
    shell_handler = RichHandler()    
    log.setLevel(log_level_name)
    shell_handler.setLevel(log_level_name)    
    fmt_shell = '%(message)s'    
    shell_formatter = logging.Formatter(fmt_shell)
    shell_handler.setFormatter(shell_formatter)
    log.addHandler(shell_handler)
    
    if len(args.logfile) > 0:
        file_handler = logging.FileHandler(args.logfile)
        file_handler.setLevel(logging.DEBUG)
        fmt_file = '%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
        file_formatter = logging.Formatter(fmt_file)
        file_handler.setFormatter(file_formatter)
        log.addHandler(file_handler)        

def main(args):

    setLogging(args)

    #Folders
    cwd = os.getcwd()
    global stacks_path, needle_path, output_path, csv_path 

    # if len(args.stacksfolder) > 0:
    #     stacks_path = args.stacksfolder
    # else:
    #     stacks_path = os.path.join(cwd, 'data','stacks')

    # if len(args.outputfolder) > 0:
    #     output_path = args.outputfolder
    # else:
    #     output_path = os.path.join(cwd, 'data','output')

    # if len(args.csvfolder) > 0:
    #     csv_path = args.csvfolder
    # else:
    #     csv_path = os.path.join(cwd, 'data','output_csv')

    stacks_path = export.checkInputFolderPath(args.stacksfolder, "stacks")
    output_path = export.checkInputFolderPath(args.stacksfolder, "output")
    csv_path = export.checkInputFolderPath(args.stacksfolder, "output_csv")

    needle_path = os.path.join(cwd, 'data','needle')      
    # export.checkFolder(output_path)
    # export.checkFolder(csv_path)

    log.debug("stacks: " + str(stacks_path))    
    log.debug("needle: " + str(needle_path))    
    log.debug("output: " + str(output_path))    
    log.debug("csv_path: " + str(csv_path)) 
    
    #Operation Mode

    #Get Image Strings from Command line
    if len(args.image) > 0 or len(args.template) > 0 :
        if os.path.isfile(args.image) & os.path.isfile(args.template):
            log.info("[bold purple]Single File Mode.  [/]", extra={"markup": True})  
            log.info("[bold green]Image: " + args.image + " [/] [bold yellow] template: " + args.template + " ", extra={"markup": True})  
            runCounter(args.image,args.template,args.tolerance,output_path)
        else:  
            log.info("[bold cyan]Single File Mode.  [/]", extra={"markup": True})  
    
            if not os.path.isfile(args.image):
                log.error("[bold red]Image File not found [/] [yellow] " + args.image + " [/]", extra={"markup": True})  

            if not os.path.isfile(args.template):    
                log.error("[bold red]template File not found [/] [yellow] " + args.template + " [/]", extra={"markup": True})  

            log.error("Exit")    

    else: #stacks folder
        log.info("[bold cyan]Folder Mode[/]", extra={"markup": True}) 

        if len(args.stacksfolder) > 0:
            log.info("[bold white]Folder: [/] " + stacks_path , extra={"markup": True}) 

        if not os.path.exists(stacks_path):
            log.error("[bold red blink]Stacks Folder not found " + stacks_path + " [/]", extra={"markup": True})  
            log.error("Exit")  
        else:  
            log.info("[bold cyan]Get all images from " + stacks_path + " [/]", extra={"markup": True})     
            allImagesMode(args.tolerance)   
    
    
              
if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args)



# All the 6 methods for comparison in a list
#methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
#            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

# 	Point  	pt1,
#		Point  	pt2,
#		const Scalar &  	color,
#		int  	thickness = 1,
#		int  	lineType = LINE_8,
#		int  	shift = 0 
#'top_left': (139, 351), 'bottom_right': (176, 382), 'center': [157.5, 366.5], 'tolerance': 0.8956932}          
#images = convert_from_path('DEL_DU_3_SI_ESEC_----_04_GR_001_05-esec.pdf')
        

#https://appdividend.com/2019/07/18/python-list-example-list-in-python-tutorial-explained/
#https://github.com/starcraft04/swauto/blob/master/functions_opencv.py
#https://iq-inc.com/importerror-attempted-relative-import/
#https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/

    
# def checkPicture(screenshot, templateFile, tolerance_list ,directories,allConfigs,multiple = False, showFound = False, saveFound = False):
    
#     #This is an intermediary function so that the actual function doesn't include too much specific arguments

#     if templateFile[:-4] in tolerance_list:
#         tolerance = float(tolerance_list[templateFile[:-4]])
#     else:
#         tolerance = float(tolerance_list['global'])

#     font = cv2.FONT_HERSHEY_PLAIN

#     #Here we will detect all files that have the same base name ex: victory.png, victory02.png, ...
#     allTemplateFiles = findAllPictureFiles(templateFile[:-4],directories['basepicsdir'])
#     result = {
#         'res': False,
#         'best_val': 0,
#         'points': [],
#         'nameVersions': [],
#         'name': templateFile,
#     }

#     for templateFileName in allTemplateFiles:

#         template = cv2.imread(os.path.join(directories['basepicsdir'],templateFileName),-1)

#         #The value -1 means we keep the file as is meaning with color and alpha channel if any
#         #   btw, 0 means grayscale and 1 is color

#         #Now we search in the picture
#         result_temp = findPicture(screenshot,template, tolerance,allConfigs, multiple)

#         if result_temp['res'] == True:
#             if result['res'] == False:
#                 result['points'] = []
#                 result['nameVersions'] = []
#             result['res'] = result_temp['res']
#             result['best_val'] = result_temp['best_val']
#             #!!!!! Attention, if the images are close to each other, there could be overlaps !!!!!!

#             for result_temp_point in result_temp['points']:
#                 overlap = False
#                 for result_point in result['points']:
#                     overlap = util.twoSquaresDoOverlap(result_point,result_temp_point)
#                     if overlap:
#                         break
#                 if not overlap:
#                     result['points'].append(result_temp_point)
#             result['nameVersions'].append(templateFileName)

#         elif result['res'] == False:
#             result['best_val'] = result_temp['best_val']
#             result['points'].extend(result_temp['points'])
#             result['nameVersions'].append(templateFileName)

#     #If it didn't get any result, we log the best value
#     if not result['res']:
#         print('Best value found for %s is: %f',templateFile,result['best_val'])
#         color_showFound = (0,0,255)
#     else:
#         logging.info('Image %s found',templateFile)
#         if logging.getLogger().getEffectiveLevel() == 10:
#             saveFound = True
#         color_showFound = (0,255,0)

#     if saveFound or showFound:
#         screenshot_with_rectangle = screenshot.copy()
#         for pt in result['points']:
#             cv2.rectangle(screenshot_with_rectangle, pt['top_left'], pt['bottom_right'], color_showFound, 2)
#             fileName_top_left = (pt['top_left'][0],pt['top_left'][1]-10)
#             cv2.putText(screenshot_with_rectangle,str(pt['tolerance'])[:4],fileName_top_left, font, 1,color_showFound,2)
#     if saveFound:
#         #Now we save to the file if needed
#         filename = time.strftime("%Y%m%d-%H%M%S") + '_' + templateFile[:-4] + '.jpg'
#         cv2.imwrite(os.path.join(directories['debugdir'] , filename), screenshot_with_rectangle)
#     if showFound:
#         cv2.imshow('showFound',screenshot_with_rectangle)
#         cv2.waitKey(0)

#     return result

# from pdf2image.exceptions import (
#     PDFInfoNotInstalledError,
#     PDFPageCountError,
#     PDFSyntaxError
# )    
