#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch
@Auther Email - bar.rose65@gmail.com

<SCRIPT EXAPLAIN>
"""
# TODO 
"""
add clean up
check for any err
"""
import argparse
from pprint import pprint
import subprocess
import os
import datetime
import sys
from logger import logger
from reader import Reader
from writer import Writer
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-crw'
# ------- # Outside Variable - visual && usefull variable # ------- #
dashLine = '-------------------------------------------'
log = logger(enableSave=False)
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
# ------- # Outside function - configParser # ------- #
def configParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e1", "--example_1", help="this is example args number 1",
                        type=str, required=False, default=None)
    parser.add_argument("-e2", "--example_2", help="this is example args number 1 - True or False",
                        required=False, action='store_true', default=False)
    return parser


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
# ------- # Class -> tamplateClass # ------- #
class Crawler():
    """
    - Exaplain :
        - Search inside all script in con folder for possible arugments

    """
    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        self.blackList = [scriptName]
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #
        self.pathFolderBase = Reader().extractorFilePathFromAlbertConfigFiles('albert')

    # ------- # Methods -> mapAllScriptsInsideTheBaseFolder # ------- #
    def mapAllScriptsInsideTheBaseFolder(self):
        """Use os.walk to detect all script path and script name inside base folder - Return dict"""
        # init basic var
        _locationFilesTypeDict = Reader().returnAllAlbertConfigFiles()
        return _locationFilesTypeDict

    # ------- # Methods -> searchScriptNickname # ------- #
    def searchScriptNickname(self, searchNickName: str):
        # init basic var
        _readMapJsonFile = Reader().jsonReader(Reader().pathAlbertConfigFiles)
        _scriptLocationTypeDict = self.mapAllScriptsInsideTheBaseFolder()
        _itemToSearch = 'scriptNickname = '
        _itemToIgnore = "scriptNickname = '-st' # scriptTemplate will be -st"
        _res = False
        # checkers
        # exists
        if searchNickName in _readMapJsonFile['crawler'].keys():
            return _readMapJsonFile['crawler'][searchNickName]['path']
        else:
            # not eixsts
            log.printLog(0, 'Deploy crawler searcher')

            for _, _scriptPath in enumerate(_scriptLocationTypeDict):
                if os.path.exists(_scriptPath) and str(_scriptPath).endswith('.py') and not [i for i in self.blackList if i in _scriptPath]:

                    _readInsideScript = Reader().readAnyTxtFile(_scriptPath)
                    for _eachRow in _readInsideScript:
                        if _itemToSearch in _eachRow and _itemToIgnore not in _eachRow:
                            _match = str(_eachRow.split(_itemToSearch)[
                                         1]).strip().replace("'", '')
                            _readMapJsonFile['crawler'][_match] = {
                                "path": _scriptPath, "lastUpdateTime": str(datetime.datetime.now())}
                            if searchNickName == _match:
                                log.printLog(
                                    1, f'Match [{searchNickName}] inside albert - set nickname to [{_match}]')
                                _res = _readMapJsonFile['crawler'][searchNickName]['path']
        if _res:
            # insert new data to map file
            log.printLog(0, 'Deploy crawler writer')
            # # write data to map json file
            Writer().writeAnyJsonFile(Reader().extractorFilePathFromAlbertConfigFiles(
                'config/albert.json'), _readMapJsonFile)
        else:
            log.printLog(
                2, f'Cannot find [{searchNickName}] in albert project folder , please make sure you add the line -> {_itemToSearch} YourScriptNickName')
        return _res

    # ------- # Methods -> configParser # ------- #
    def configParser(
            self,
            exampleToHowToRunScriptTypeBool: bool = False):
        # init basic var
        _readMapJsonFile = Reader().jsonReader(Reader().pathAlbertConfigFiles)
        _parser = ThrowingArgumentParser()
        if exampleToHowToRunScriptTypeBool:
            _exampleText = exampleToHowToRunScriptTypeBool
            _parser = ThrowingArgumentParser(epilog=_exampleText,
                                             formatter_class=argparse.RawDescriptionHelpFormatter)

        _extractDataFromCrawlerListData = {}
        for nickname in _readMapJsonFile['crawler'].keys():
            _extractDataFromCrawlerListData[nickname] = _readMapJsonFile['crawler'][nickname]['path']
        # start looping items
        for _eachKey, _eachValue in _extractDataFromCrawlerListData.items():

            _eachValueBaseName = os.path.basename(
                _eachValue).replace('.py', '')

            _parser.add_argument(
                f'{_eachKey}',
                f'--{str(_eachValueBaseName).replace("-","")}',
                action='store_true',
                help=f'Call the script [{_eachValueBaseName}] ',
                required=False,
                default=None
            )

        return _parser


if __name__ == "__main__":
    # # ./_crawler.py sudo -ssh "ladh1234" -t "123" -m "456"
    # # ./_crawler.py sudo -command -t 123 "1;"
    # # init basic var
    _sysArgv = sys.argv
    _runAsSudo = False
    _scriptCaller = ''
    _scriptArguemnts = ''
    _scriptPathFromCrwler = ''
    _fullCrwlerCommandToExec = ''
    # check if sudo is needed
    if 'sudo' in _sysArgv[1]:
        _runAsSudo = 'sudo'
        _scriptCaller = str(_sysArgv[2]).strip()
        _scriptArguemnts = ' '.join(_sysArgv[3:])
    if 'sudo' not in _sysArgv[1]:
        _runAsSudo = ''
        _scriptCaller = str(_sysArgv[1]).strip()
        _scriptArguemnts = ' '.join(_sysArgv[2:])
    # extract script path
    if _scriptCaller == '-h':
        pass
    else:
        # call the script via os.system
        _scriptPathFromCrwler = Crawler().searchScriptNickname(_scriptCaller)
        if _scriptPathFromCrwler:
            _fullCrwlerCommandToExec = f'{str(_runAsSudo).strip()} python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip(
            )
            log.printLog(
                0, f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
            os.system(_fullCrwlerCommandToExec)
            exit(0)
    try:
        # show possible args
        args = Crawler().configParser().parse_args()

    except ValueError:
        pass
