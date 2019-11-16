# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:41:21 2017

@author: 425196
"""

import re
from re import compile

#import FileChooser
#from FileChooser import selectFile
#xlTargetFile = selectFile()    
xlTargetFile = "/Users/taagebert/github/Python/Karina/BehavioralDataProcs/Data/Results.xlsx"
    
#import FolderChooser
#from FolderChooser import selectFolder
folderPath = "/Users/taagebert/github/Python/Karina/BehavioralDataProcs/Data/InputData"

#folderPath = selectFolder()

import openpyxl
from openpyxl import load_workbook
wb = load_workbook(xlTargetFile)
sheet = wb["Data"]

from openpyxl.utils.dataframe import dataframe_to_rows

import importlib
from importlib import reload

import DataFileProcessor
reload(DataFileProcessor)
from DataFileProcessor import processDataFile

import os    
    
for root, dirs, files in os.walk(folderPath): 
    if u'Extra Data' not in root: 

        for file_ in files:
            if u'.xlsx' in file_ and (u'RateEmotion' in file_ or u'RateArousal' in file_):
                
                if u'RateEmotion' in file_:
                    suffix = "E"
                elif u'RateArousal' in file_:
                    suffix = "A"
                else: raise ValueError('Error determining file type for: ' + file_)

                #Invoke the 'ProcessDataCsv' procedure, returning a data frame
                print("Processing file: ", file_)
                df = processDataFile (file_, os.path.join(root, file_), suffix)

                if len(df) > 0:
                    print("About to write to target workbook.  Dataframe length = " + str(len(df)))
                    #Write dataframe rows to spreadsheet
                    for r in dataframe_to_rows(df, index=False, header=False) : 
                        sheet.append(r)
                        

                
    
wb.save(xlTargetFile)

print("Finished")
