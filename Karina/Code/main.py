# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:41:21 2017

@author: 425196
"""

import re
from re import compile

import FileChooser
from FileChooser import selectFile
#xlTargetFile = selectFile()    
xlTargetFile = "/Users/taagebert/Documents/Work/Python/Karina/SummaryData.xlsx"
    
import FolderChooser
from FolderChooser import selectFolder
folderPath = "/Users/taagebert/Documents/Work/Python/Karina/DataFiles2"
#folderPath = selectFolder()

import openpyxl
from openpyxl import load_workbook
wb = load_workbook(xlTargetFile)
#sheet = wb.get_sheet_by_name('Data')
sheet = wb["Data"]

from openpyxl.utils.dataframe import dataframe_to_rows

import importlib
from importlib import reload

import CsvDataProcessor
reload(CsvDataProcessor)
from CsvDataProcessor import processDataCsv

import os    
    
for root, dirs, files in os.walk(folderPath): 
    if u'Extra Data' not in root: 
        #initialize the PRE/POST variable
        prefix = ""
        murfiTmstmp = ""
        for file_ in files:
            if u'.csv' in file_ and u'MURFI' in file_:
                tmstmpRegex = re.compile(r'\d\d\d\d(_\d)?.csv')
                tmstmp = tmstmpRegex.search(file_)
                if tmstmp is not None:
                    murfiTmstmp = str(tmstmp.group())[:4]
                    print('MURFI tmstmp: ' + murfiTmstmp)

        for file_ in sorted(files):
            #if u'.csv' in file_ and u'exclude' not in file_ and u"MURFI" in file_: 
            if u'.csv' in file_ and u'exclude' not in file_ : 
                #Derive Timestamp of current file
                fileTmstmp = ""
                regexRslt = tmstmpRegex.search(file_)
                assert(regexRslt is not None), "Timestamp couldn't be derived from FileName: " + csvDataFileName
                fileTmstmp = str(regexRslt.group())[:4]
                
                #Compare current file timestamp to MURFI file timestamp to determine PRE vs POST
                if u"MURFI" in file_:
                    prefix = "FB"
                elif fileTmstmp != "" and murfiTmstmp != "":
                    if fileTmstmp <= murfiTmstmp:
                        prefix = "PRE"
                    else: prefix = "POST"                    
                elif prefix == "": prefix = "PRE"
                elif prefix == "PRE": prefix = "POST"
                else: raise Exception("File category couldn't be derived for file: " + file_)

                #Invoke the 'ProcessDataCsv' procedure, returning a data frame
                print("Processing file: ", file_, " as '", prefix, "'")
                df = processDataCsv (file_, os.path.join(root, file_), prefix)

                if len(df) > 0:
                    print("About to write to target workbook.  Dataframe length = " + str(len(df)))
                    #Write dataframe rows to spreadsheet
                    for r in dataframe_to_rows(df, index=False, header=False) : 
                        sheet.append(r)
                        
                else:   #If no data was found then reset the 'prefix' variable
                    if prefix == "PRE": prefix = ""
                    elif prefix == "POST": prefix = "PRE"
                
    
wb.save(xlTargetFile)

print("Finished")
