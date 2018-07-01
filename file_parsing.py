# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 01:10:12 2018

Project Title : Weather Forecasting using AI

@author : Mohammad Noor Ul Hasan

last Edit : Fri Jun 29  2018

Title : File Parsing


"""

#to use this class :
#   create a object of class FileParsing with the address of file
#   obj = FileParsing(r"..\..\Data Set\data set.txt")
#   print(obj.DF)

import pandas as pd
class FileParsing:
    #Doc String of the class
    "This class is used to parse the Radar Raw file"
    
    #Declaration Of variable
    _totalColumns = 0
    
    #variable to store file 
    
    #Counting Variables
    _headerLineCount = 0
    _footerlineCount = 0
    
    #List Variables
    _Az = []
    _El = []
    _value = []
    _DFIndex = []
    _time = []
    
    #Data Frame Variables
    #DF is abbrevation for Data Frame
    
    def __init__(self,fileName):
        self._file = open(fileName,"r").read()
        self._fileCleaning()
        self._fileLinesCleaning()
        self._headerLineCount = self._headerLineCounting()
        self._footerlineCount = self._footerLineCounting()
        self._file = self._file[self._headerLineCount+1:-1*(self._footerlineCount+1)]
        self._extractingInformation()
        self._extractingValues()
        self._createDataFrames()
        self.insertNAN()
        self._printDataFrame()
    
    def _fileCleaning(self):
        self._file = self._file.replace("\n\n\n","\n")
        self._file = self._file.replace("\n\n","\n")
        self._file = self._file.split("\n") 
        
    def _headerLineCounting(self):
        lineCount = 0 
        for fileLine in self._file:
            if fileLine:
                if fileLine[0] is "#":
                    break;
                else:
                    lineCount += 1
        return lineCount
    
    def _footerLineCounting(self):
        lineCount = 0
        for reverseIndex in range(1,len(self._file)):
            if self._file[-1*reverseIndex]:
                if 'Sweep began' not in self._file[-1*reverseIndex]:
                    break
                else:
                    lineCount += 1
        return lineCount
    
    def _fileLinesCleaning(self):
        file = []
        for fileLine in self._file:
            fileLine = str(fileLine)
            fileLine = fileLine.strip(" ")
            fileLine = fileLine.replace("   "," ")
            fileLine = fileLine.replace("  "," ")
            fileLine = fileLine.replace(",","")
            file.append(fileLine)
        
        self._file = file
    
    def _extractingInformation(self):
        Az = []
        El = []
        index = []
        time = []
        
        for fileLine in self._file[::2]:
            splitedFileLine = fileLine.split(" ")
            Az.append( list(splitedFileLine[2:4]) )
            El.append( list(splitedFileLine[5:7]) )
            index.append(splitedFileLine[0][1:])
            time.append(splitedFileLine[-1])
        self._Az = Az;
        self._El = El;
        self._DFIndex = index;
        self._time = time
    
    def _extractingValues(self):
        value = []
        for fileLine in self._file[1::2]:
            splitedFileLine = fileLine.split(" ")
            value.append(list(splitedFileLine))
            self._value = value 
        self._totalColumns = len(self._file[1].split(" "))
        
    def _createDataFrames(self):
        self.valueDF = pd.DataFrame(self._value,columns = ["value"+str(i+1) for i in range(self._totalColumns)], index = self._DFIndex)
        self.timeDF = pd.DataFrame(self._time,columns = ["Time"], index = self._DFIndex)
        self.AzDF = pd.DataFrame(self._Az,columns = ["Az_r1","Az_r2"], index = self._DFIndex)
        self.ElDF = pd.DataFrame(self._El, columns = ["El1","El2"], index = self._DFIndex)
        frames  = [self.timeDF,self.AzDF,self.ElDF,self.valueDF]
        self.DF= pd.concat(frames,axis = 1)
    
    def _printDataFrame(self):
        print(self.DF)
