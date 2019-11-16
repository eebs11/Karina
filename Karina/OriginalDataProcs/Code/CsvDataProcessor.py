# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 15:44:07 2017

Revised on Dec 17 2018
"""

def processDataCsv (csvDataFileName, csvDataFilePath, fileType):

    import pandas as pd
    import numpy as np
    
    import re
    from re import compile    
    
    #Read the INPUT csv file to a Data Frame
    df = pd.read_csv(csvDataFilePath)
    
    varNames = []
    varVals = []
    varTypes = []
    
    #Initalize the OUTPUT DataFrame
    oDf = pd.DataFrame()

    if len(df) == 0 : 
        raise ValueError("No data frame content for file: " + csvDataFileName)
 
    #Define column header names for Response / Response Time
    if fileType == 'FB':    #MURFI Feedback file type
        dataLevel = 'section'
        
        imageColName = 'image2'
        keyColName = 'key_resp_2.keys'
        rtColName = 'key_resp_2.rt' 
                   
    else:
        dataLevel = 'row'
        
        imageColName = 'image'
        keyColName = 'response.keys'
        rtColName = 'response.rt'
    
    #Validate that Column titles exist in data file    
    assert(imageColName in df.columns), "Column name: '" + imageColName + "' not present in dataframe"
    assert(keyColName in df.columns or rtColName in df.columns), "RT Column names '" + keyColName + "'/'" + rtColName + "' not present in dataframe"    
            
    #Match the 1st 4 (or more) digits of the FileName to get the Participant ID
    regexSearch = re.compile(r'^\d{4,}')
    regexRslt = regexSearch.search(csvDataFileName)
    assert(regexRslt is not None), "Participant ID couldn't be derived from FileName: " + csvDataFileName

    #Participant ID
    ptcptId = regexRslt.group()
    
    #Initialize tracking variables
    imageFileName = ''
    hiLow = 'Hi'
    seqNum = 1
    
    emotion = ''
    selfPct = ''
    exception = ''
    

    #For each row in the data frame...
    for i in df.index:
        
        #If not a blank row
        if pd.notnull(df[imageColName][i]) :

            #Determine current row image file name w/ regular expression pattern match
            regexSearch = re.compile(r'/\w+.jpg$')
            regexRslt = regexSearch.search(df[imageColName][i])
            assert(regexRslt is not None), "Image File Name couldn't be derived from text: " + df[imageColName][i]
            
            imageFileName = str(regexRslt.group())[1:]        

            #Emotion
            if imageFileName[:2] == u'ha': 
                emotion = "Happy"
            elif imageFileName[:2] == u'sa': 
                emotion = "Sad"
            elif imageFileName[:3] == u'neu': 
                emotion = "Neutral"
            else : raise ValueError('Could not determine emotion state from Image File Name: ' + imageFileName)

            #SelfPct    
            selfPct = (str(int(df['percentSelf'][i] * 100)))

            #SelfPct Exceptions
            if hiLow == "Hi" and int(selfPct) < 65 : exception = "Lo"
            elif hiLow == "Lo" and int(selfPct) >= 65 : exception = "Hi"
            else : exception = ""

            if dataLevel == 'row':
            
                #Response Times
                if rtColName in df.columns :    
                    varTypes.append("RTT")
                    varVals.append(df[rtColName][i])

                    #VarName = {PRE/POST}_{Happy, Sad, Neutral}{Hi,Lo}{Lo,Hi}_(1,2,3,...)_[0-100]_{RTT,ACC}                
                    varNames.append(fileType + "_" + emotion + hiLow + exception + '_' + str(seqNum) + '_' + selfPct + '_' + varTypes[-1])
                    
                #Response Keys
                if keyColName in df.columns :    
                    varTypes.append("ACC")

                    if df[keyColName][i] != "None" and pd.notnull(df[keyColName][i]): varVals.append(int(df[keyColName][i]))
                    else: varVals.append(0)
                
                    #VarName = {PRE/POST}_{Happy, Sad, Neutral}{Hi,Lo}{Lo,Hi}_(1,2,3,...)_[0-100]_{RTT,ACC}                
                    varNames.append(fileType + "_" + emotion + hiLow + exception + '_' + str(seqNum) + '_' + selfPct + '_' + varTypes[-1])
                
                
                seqNum += 1

            
        else :
            if imageFileName != '':  #Ignore blank lines at top of file
        
                #Write-out section-level data if appropriate(i.e. MURFI feedback)
                if dataLevel == 'section':
                    #Response Times
                    if rtColName in df.columns :    
                        varTypes.append("RTT")

                        if df[rtColName][i] != "None" and pd.notnull(df[rtColName][i]): varVals.append(df[rtColName][i])
                        else: varVals.append(-9999)
    
                        #VarName = "RateEmotion"_{Happy}{Hi,Lo}_(1,2,3,4)_{RTT,ACC}                
                        varNames.append('RateEmotion' + emotion + hiLow + '_' + str(seqNum) + '_' + varTypes[-1])
                        
                    #Response Keys
                    if keyColName in df.columns :    
                        varTypes.append("ACC")
    
                        if df[keyColName][i] != "None" and pd.notnull(df[keyColName][i]): varVals.append(int(df[keyColName][i]))
                        else: varVals.append(-9999)
                    
                        #VarName = "RateEmotion"_{Happy}{Hi,Lo}_(1,2,3,4)_{RTT,ACC}                
                        varNames.append('RateEmotion' + emotion + hiLow + '_' + str(seqNum) + '_' + varTypes[-1])

                    #Increment every second section, as inidicated by Hi, Lo, Hi, Lo, ... sequence
                    if hiLow == "Lo":
                        seqNum += 1
                    
                elif dataLevel == 'row':                            
                    seqNum = 1

                #Toggle HiLo w/ each new section
                if hiLow == "Lo": 
                    hiLow = "Hi"  
                else: hiLow = "Lo"
    

    
    oDf['varNames'] = varNames
    oDf['varVals'] = varVals
    oDf['varTypes'] = varTypes    

    oDf['ptcptId'] = ptcptId
    oDf['fileNames'] = csvDataFileName
    oDf['fileCategory'] = fileType
    
    return oDf
                