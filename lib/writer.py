#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<SCRIPT EXAPLAIN>
"""
import argparse
import json
import os
import datetime
from logger import logger
from reader import Reader

# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-wj'
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
dashLine = '-------------------------------------------'
currentSite = 'site_0'
log = logger(enableSave=False)
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
# ------- # Outside function - configParser # ------- #
def configParser():
    """
    """
    parser = argparse.ArgumentParser(description='Simple example')
    parser.add_argument("-jp", "--json_path", help="what is the json path for reading ?", type=str, required=False, default=None)
    parser.add_argument("-dd", "--dict_data", help="what is the dict data to write ? ",  required=False, default=None)
    parser.add_argument("-wcdj", "--write_con_deploy_json", help="write file con_deploy_hosts.json", required=False, action='store_true', default=False)
    parser.add_argument("-wmj", "--write_map_json", help="write file map.json", required=False, action='store_true', default=False)
    parser.add_argument("-wpj", "--write_private_json", help="write file private dns.json", required=False, action='store_true', default=False)
    parser.add_argument("-waj", "--write_any_json", help="write file json file - needed location",  action='store_true',required=False, default=False)
    return parser
# ------- # Class -> Writer # ------- #
class Writer():
    """
    - Exaplain :
        - write to map json file / any other json file
    """
    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #

    # ------- # Methods -> writeAnyJsonFile # ------- #
    def writeAnyJsonFile(self,jsonFileLocationTypeStr:str,dataToWriteTypeDict:dict):
        with open(jsonFileLocationTypeStr,'w') as writeJsonFile:
            json.dump(dataToWriteTypeDict,writeJsonFile,indent=1)
            
    # ------- # Methods -> writeAnyJsonFile # ------- #
    def _writeAnyJsonFile(self,jsonFileLocationTypeStr:str,dataToWriteTypeDict:dict):
        with open(jsonFileLocationTypeStr,'w') as writeJsonFile:
            json.dump(dataToWriteTypeDict,writeJsonFile,indent=1)
            
    # ------- # Methods -> writeAnyTxtFile # ------- #
    def writeAnyTxtFile(self,textPathLoactionTypeStr:str,dataToWriteTypeList:list):
        with open(textPathLoactionTypeStr,'w') as writeTextFile:
            for _eachRow in dataToWriteTypeList:
                writeTextFile.write(str(_eachRow).strip()+'\n')

    