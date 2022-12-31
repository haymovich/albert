#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<SCRIPT EXAPLAIN>
"""
import os
import sys
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(pathScriptFolder, 'lib'))
from utils import Utils
from aliasManager import AliasManager
from logger import logger
from reader import Reader
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-setup' 
log = logger(False)

if __name__ == "__main__":
    _commamds = [
        
        f'cp -r {Reader().extractorFilePathFromAlbertConfigFiles("config/albert_tmp.json")} {os.path.join(Reader().extractorFilePathFromAlbertConfigFiles("config"),"albert.json")}',
        f'chmod -R 777 {Reader().extractorFilePathFromAlbertConfigFiles("albert")}',
    ]
    for _eachCommand in _commamds:
        os.system(_eachCommand)
    # start install /setup
    Utils().spliter()
    Utils().installLib() # install all neded lib
    Utils().checkLib() # check if all lib are install
    Utils().spliter()
    AliasManager().injectAlbertAlias() # set alias for alb /albert --> FolderPath/albert.py
    Utils().spliter()
    Utils().deployCommandSubprocess("sudo chown -R $(echo $USER) ./ ")

    log.printLog(1,'Finish install all albert req files / alias / etc - it\'s recomended to do bash after.')
    