#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<Merage all methods that similar to each other like total time for action , do while loop for action , etc...>
"""
import argparse
import subprocess
import os
import time
import datetime
import random
import json
import platform
from logger import logger
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
log = logger()
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
# ------- # Class -> tamplateClass # ------- #
class Utils():
    """
    - Exaplain :
        - Example this tamplate class
    """
    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        self.dashLine = '-------------------------------------------'
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #

    # ------- # Methods - changeTerminalName # ------- #
    def checkOsPlatform(self):
        """check the os platform on the host --> 1=linux | 2=mac | 3=windows | False=unknow"""
        _checkOs = platform.system()
        _res = 4
        if _checkOs == 'Linux':
            _res = 1
        if _checkOs == 'Darwin':
            _res = 2 
        if _checkOs == 'Windows':
            _res = 3
        
        return _res
            
    # ------- # Methods -> deployCiLinkFolder # ------- #
    def deployCommandSubprocess(self,commandToDeploy:str,silenceMode:bool=False,enablePrint:bool=True):
        _commandToDeploy = commandToDeploy.strip()
        _rc,_out = subprocess.getstatusoutput(_commandToDeploy)
        if int(_rc) == 0:
            if enablePrint:
                log.printLog(1,'Command was return without any error.')
        else:
            if enablePrint:
                log.printLog(2,f'Command was return with error. {_out}')
        return _out
    # ------- # Methods - changeTerminalName # ------- #
    def checkPathExists(self,pathToCheck:str):
        if os.path.exists(pathToCheck):
            return True

        else:
            return False
    # ------- # Methods - changeTerminalName # ------- #
    def extractAllUsernamesInCurrentMachine(self):
        blackList = ['daemon','root','nobody']
        mapCommads = {
            1:"etent passwd | grep /bin/bash | cut -d: -f1",#linux
            2:"dscl . list /Users | grep -v _", #mac
            3:False,
            4:False
        }
        _res = False
        if self.checkOsPlatform() != 3 or self.checkOsPlatform() != 4: 
            _res = [i for i in self.deployCommandSubprocess(mapCommads[self.checkOsPlatform()],enablePrint=False).split('\n') if i not in blackList]
        return _res
    # ------- # Methods - extractItemFromSysArgv # ------- #
    def extractItemFromSysArgv(
        self,
        sysArgvToSearchingTypeList:list,
        indexToFindTypeStr:str,
        firstNumberAddToIndexTypeInt:int=0,
        secondNumberAddToIndexTypeInt:int=0,
        defualtResultsToReturnTypeAny:any=False
        ):
        # init basic var
        _sysArgvToSearchingTypeList = sysArgvToSearchingTypeList
        _indexToFindTypeStr = indexToFindTypeStr
        _firstNumberAddToIndexTypeInt = firstNumberAddToIndexTypeInt
        _secondNumberAddToIndexTypeInt = secondNumberAddToIndexTypeInt
        _results = defualtResultsToReturnTypeAny
        # checking
        try:
            if _indexToFindTypeStr in _sysArgvToSearchingTypeList:
                _indexForMatchItem = _sysArgvToSearchingTypeList.index(_indexToFindTypeStr)
                _firstNumberAddToIndexTypeInt = _indexForMatchItem+_firstNumberAddToIndexTypeInt
                _secondNumberAddToIndexTypeInt = _indexForMatchItem+_secondNumberAddToIndexTypeInt
                _results = str(_sysArgvToSearchingTypeList[_firstNumberAddToIndexTypeInt:_secondNumberAddToIndexTypeInt][0]).strip()
        except IndexError:
            pass
        return _results
    # ------- # Methods - extractItemFromSysArgvAdvnace # ------- #
    def extractItemFromSysArgvAdvnace(
        self,
        sysArgvToSearchingTypeList:list,
        startIndex:str,
        stopAt:str='n',
        defualtResultsToReturnTypeAny:any=False
        ):
        # init basic var
        _sysArgvToSearchingTypeList = sysArgvToSearchingTypeList
        _startIndex = startIndex
        _stopAt = stopAt
        _results = defualtResultsToReturnTypeAny
        _startIndexMatch = False
        _stopIndexMatch = False
        # checking
        try:
            if _startIndex in _sysArgvToSearchingTypeList:
                _startIndexMatch = _sysArgvToSearchingTypeList.index(_startIndex)+1
                if _stopAt == 'n':
                    _stopIndexMatch = len(_sysArgvToSearchingTypeList)+1
                if _stopAt in _sysArgvToSearchingTypeList:
                    _stopIndexMatch = _sysArgvToSearchingTypeList.index(_stopAt)
            if  _stopIndexMatch and _stopIndexMatch:
                _results = str(_sysArgvToSearchingTypeList[_startIndexMatch:_stopIndexMatch][0]).strip()
        except IndexError:
            pass
        return _results

    # ------- # Methods - iniParser # ------- #
    def iniLoader(self,pathForIniFile:str):
        """Load any ini file"""
        if not os.path.exists(pathForIniFile):
            print(f'Please make sure ini file [{pathForIniFile}] exists.')
        print('exists')

    # ------- # Methods - iniParser # ------- #
    def iniLoader(self,pathForIniFile:str):
        """Load any ini file"""
        if not os.path.exists(pathForIniFile):
            print(f'Please make sure ini file [{pathForIniFile}] exists.')
        print('exists')
        
    # ------- # Methods - jsonLoader # ------- #
    def jsonLoader(self,pathForFile:str):
        """Load any ini file"""
        if not os.path.exists(pathForFile):
            print(f'Please make sure json file [{pathForFile}] exists.')
        with open(pathForFile,'r') as jsonReader:
            return json.load(jsonReader)
        
if __name__ == "__main__":
    # test start and ended time
    # start
    _titleNameForStart = 'This is test vfr 1'

