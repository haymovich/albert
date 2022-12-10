#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<SCRIPT EXAPLAIN>
"""
import argparse
import subprocess
import os
import datetime
import sys
from utils import Utils

# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
dashLine = '-------------------------------------------'
currentSite = 'site_0'

# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
# ------- # Outside function - projectMapper # ------- #
def projectMapper():
    """loop over all project folder and automatic return all files / folder exists."""
    pathAlbertHomeDir = os.path.dirname(pathScriptFolder)
    blackListDirsForMapper = [
        '.git', '__pycache__', '.cpython-', '.log']
    pathProjectParser = {}
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
            # folders
            if _dirBaseName not in pathProjectParser.keys():
                pathProjectParser[_dirBaseName] = dirs+'/'
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
            '.git', '__pycache__', '.cpython-', '.log']
        self.pathProjectParser = projectMapper()
        self.pathAlbertConfigFiles = self.pathProjectParser['config/albert.json']

    # ------- # Methods -> jsonReader # ------- #
    def jsonReader(self, pathForFile: str):
        """Read any json file"""
        return Utils().jsonLoader(pathForFile=pathForFile)
    # ------- # Methods -> showAllKeysInConfigFilesMapper # ------- #

    def showAllKeysInConfigFilesMapper(self):
        for k, v in self.pathProjectParser.items():
            print(f'{k} ----> {v}')
    # ------- # Methods -> filePathExtractorFromAlbertConfigFiles # ------- #

    def extractorFilePathFromAlbertConfigFiles(self, keyToExtract: str):
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
        print(Reader().extractorFilePathFromAlbertConfigFiles('log'))
        print(dashLine)
        print("Reader().showAllKeysInConfigFilesMapper()")
        # print(Reader().showAllKeysInConfigFilesMapper())
        # pass
