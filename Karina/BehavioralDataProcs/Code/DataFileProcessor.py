# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 15:44:07 2017

Revised on Dec 17 2018
"""

def processDataFile (dataFileName, dataFilePath, fileType):

    import pandas as pd
    import numpy as np
    
    import re
    from re import compile    
    
    df = pd.read_excel(dataFilePath, sheet_name = 0, skiprows=1, usecols=[1,17,19])
    
    #Read the INPUT csv file to a Data Frame
    #df = xl.parse(xl.sheet_names[0])
    
    varNames = []
    varVals = []
    ptcptIds = []
    
    #Initalize the OUTPUT DataFrame
    oDf = pd.DataFrame()

    if len(df) == 0 : 
        raise ValueError("No data frame content for file: " + dataFileName)
 
    #Define column header names  
    subjColName = 'Subject'      
    imageColName = 'Pic'
    
    if fileType == 'A':
        respColName = 'RateExcitement.RESP'
    elif fileType == 'E':
        respColName = 'RateEmotion.RESP'
    else: raise ValueError('Invalid file type: ' + fileType)
    
    #Validate that Column titles exist in data file    
    assert(subjColName in df.columns), "Column name: '" + subjColName + "' not present in dataframe"
    assert(imageColName in df.columns), "Column name: '" + imageColName + "' not present in dataframe"
    assert(respColName in df.columns), "Column name: '" + respColName + "' not present in dataframe"
            
#    #Match the 1st 4 (or more) digits of the FileName to get the Participant ID
#    regexSearch = re.compile(r'^\d{4,}')
#    regexRslt = regexSearch.search(dataFileName)
#    assert(regexRslt is not None), "Participant ID couldn't be derived from FileName: " + dataFileName
#
#    #Participant ID
#    ptcptId = regexRslt.group()
    

    #For each row in the data frame...
    for i in df.index:
        
        #If not a blank row
#        if pd.notnull(df[imageColName][i]) :

        #Determine current row image file name w/ regular expression pattern match
        regexSearch = re.compile(r'/\w+.(bmp|jpg)$')
        regexRslt = regexSearch.search(df[imageColName][i])
        assert(regexRslt is not None), "Image File Name couldn't be derived from text: " + df[imageColName][i]        
        imageFileName = str(regexRslt.group())[1:]
        
        #Remove file extension
        imageFileName = imageFileName[0:len(imageFileName) - 4]

        #Determine current row reaction type w/ regular expression pattern match
        regexSearch = re.compile(r'\w+/(\w+)/.*$')
        regexRslt = regexSearch.search(df[imageColName][i])
        assert(regexRslt is not None), "Reaction Type couldn't be derived from text: " + df[imageColName][i]        
        reactType = str(regexRslt.group(1))
        
        varNames.append(reactType + '_' + imageFileName + '_' + fileType)
        
        varVals.append(df[respColName][i])
        
        ptcptIds.append(df[subjColName][i])

    
    oDf['varNames'] = varNames
    oDf['varVals'] = varVals
    oDf['ptcptId'] = ptcptIds
    
    return oDf
                