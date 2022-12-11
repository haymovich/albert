#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<SCRIPT EXAPLAIN>
alb -reader -show   
"""
import json
import argparse
import subprocess
import os
import datetime
import sys
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-reader'
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
dashLine = '-------------------------------------------'
currentSite = 'site_0'

# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
# ------- # Outside function - projectMapper # ------- #
def projectMapper(returnOnlyFilePath:bool=False):
    """loop over all project folder and automatic return all files / folder exists."""
    pathAlbertHomeDir = os.path.dirname(pathScriptFolder)
    blackListDirsForMapper = [
        '.git', '__pycache__', '.cpython-', '.log','.md','__init__.py']
    pathProjectParser = {}
    pathProjectParserOnlyFiles = []
    for dirs, _, files in os.walk(pathAlbertHomeDir, topdown=True):
        _dirBaseName = os.path.basename(dirs)
        if not [i for i in blackListDirsForMapper if i in dirs]:
            # files
            for file in files:
                _filePath = os.path.join(dirs, file)
                if not [i for i in blackListDirsForMapper if i in _filePath]:
                    if file not in pathProjectParser.keys():
                        dirName = os.path.dirname(
                            _filePath).rsplit("/")[::-1][0]
                        pathProjectParser[f'{dirName}/{file}'] = _filePath
                        if '.' in  _filePath:
                            pathProjectParserOnlyFiles.append(_filePath)
            # folders
            if _dirBaseName not in pathProjectParser.keys():
                pathProjectParser[_dirBaseName] = dirs+'/'
    if returnOnlyFilePath:
        return pathProjectParserOnlyFiles
    
    return pathProjectParser
# ------- # Outside function - configParser # ------- #


def configParser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-show", "--show", help="show examples",
                        action='store_true', required=False, default=False)
    return parser
# ------- # Class -> Reader # ------- #


class Reader():
    """
    - Exaplain :
        - Example this tamplate class
    """
    def __init__(self):

        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #
        self.pathAlbertHomeDir = os.path.dirname(pathScriptFolder)
        self.blackListDirsForMapper = [
            '.git', '__pycache__', '.cpython-', '.log','__init__.py']
        self.pathProjectParser = projectMapper()
        self.pathAlbertConfigFiles = self.pathProjectParser['config/albert.json']

    # ------- # Methods -> readAlbertConfigFiles # ------- #
    def readAlbertConfigFiles(self):
        """Read any json file"""
        return self.jsonReader(pathForFile=self.pathAlbertConfigFiles)
    
    # ------- # Methods -> jsonReader # ------- #
    def jsonReader(self, pathForFile: str):
        """Read any json file """
        _res = False
        if not os.path.exists(pathForFile):
            print(f'Please make sure json file [{pathForFile}] exists.')
        with open(pathForFile,'r') as jsonReader:
            _res = json.load(jsonReader)
        return _res
    
    # ------- # Methods -> returnAllAlbertConfigFiles # ------- #
    def returnAllAlbertConfigFiles(self):
        return projectMapper(returnOnlyFilePath=True)
    
    # ------- # Methods -> showAllKeysInConfigFilesMapper # ------- #
    def showAllKeysInConfigFilesMapper(self):
        for k,v in self.pathProjectParser.items():        
            _findSpace = 45 - len(f'Arguemnt [{k}]')
            print(f'[{k}] {" "*_findSpace} is eq to [{v}]')
            
    # ------- # Methods -> readAnyTxtFile # ------- #
    def readAnyTxtFile(self,fileTxtLocationToRead:str):
        try:
            with open(fileTxtLocationToRead,'r') as readAnyTxtFile:
                return readAnyTxtFile.read().splitlines()
        except:
            pass
            # print('error')
    # ------- # Methods -> filePathExtractorFromAlbertConfigFiles # ------- #
    def extractorFilePathFromAlbertConfigFiles(self, keyToExtract: str):
        """
        Give key and extract the path for this key - for example :\n
        _path = Reader().extractorFilePathFromAlbertConfigFiles('ablert/albert.py')

        """
        _res = False
        if keyToExtract in self.pathProjectParser.keys():
            _res = self.pathProjectParser[keyToExtract]
        else:
            print(f'Error , cannot file key [{keyToExtract}]')
        return _res


if __name__ == "__main__":

    args = configParser().parse_args()
    # ------- # Arguments -> -e1 -> example 1 # ------- #
    if args.show:
        # print("Reader().extractorFilePathFromAlbertConfigFiles('config/albert.json')")
        # print(Reader().extractorFilePathFromAlbertConfigFiles('config/albert.json'))
        # print(Reader().extractorFilePathFromAlbertConfigFiles('log'))
        # print(dashLine)
        # print("Reader().showAllKeysInConfigFilesMapper()")
        Reader().showAllKeysInConfigFilesMapper()
        # pass
