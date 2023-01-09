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
scriptNickname = '-crw2'
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
    def checkForDuppInNicknames(self):
        """
        map all config file and check if any dupp in the path for any crawelers
        1. check for dup
        2. check if path exists
        3. grab all dupp values and the with the latest date , save it - all others - del
        4. save the new config json
        """
        # init basic vars
        _readMapJsonFile = Reader().readAlbertConfigFiles()
        _mapper = {}
        _res = []
        _resAsDict = {}
        _finalRes = {}
        _removeItems = set()
        # create parser for dup and file exists
        for nickname, dictItems in _readMapJsonFile['crawler'].items():
            # print({dictItems['path']:nickname})
            if os.path.exists(dictItems['path']):
                if dictItems['path'] not in _mapper.keys():
                    _mapper[dictItems['path']] = {dictItems["lastUpdateTime"]: {
                        "nickname": nickname, 'path': dictItems['path'], "lastUpdateTime": dictItems["lastUpdateTime"]}}
                else:
                    if _mapper[dictItems['path']] not in _res:
                        _res.append(_mapper[dictItems['path']])
                    _res.append({dictItems["lastUpdateTime"]: {
                                "nickname": nickname, 'path': dictItems['path'], "lastUpdateTime": dictItems["lastUpdateTime"]}})
        # commbine all dict into 1 and remove the nickname that going to stay
        for d in _res:
            _resAsDict.update(d)
            _removeItems.add(list(d.values())[0]['nickname'])
        # if _resAsDict match
        if _resAsDict:
            _dates = sorted([i for i in _resAsDict], reverse=True)[0]
            _finalRes = _resAsDict[_dates]
            _finalRes = {
                _finalRes['nickname']: {
                    'path': _finalRes['path'],
                    'lastUpdateTime': _finalRes['lastUpdateTime']
                }
            }
            _nickname = list(_finalRes.keys())[0]
            # remove the nickname that going to stay
            _removeItems.remove(_nickname)
            for _ in _removeItems:
                # pop the ones that not going to stay.
                _readMapJsonFile['crawler'].pop(_)

            # update the config
            _readMapJsonFile['crawler'][_nickname] = _finalRes[_nickname]
            # write into new file
            Writer().writeAnyJsonFile(Reader().extractorFilePathFromAlbertConfigFiles(
                'config/albert.json'), _readMapJsonFile)

    # ------- # Methods -> searchScriptNickname # ------- #

    def searchScriptNickname(self, searchNickName: str):
        """verify that the json config file is up to date and the nickname is exists"""
        _extractPath = self.searchScriptNicknameExtractor(searchNickName)
        _readMapJsonFile = Reader().readAlbertConfigFiles()
        if not os.path.exists(_extractPath):
            log.printLog(
                2, f'Seems like the Path [{_extractPath}] for script nickname [{searchNickName}] has change - deploy auto rescan.')
            _readMapJsonFile['crawler'].pop(searchNickName)
            Writer().writeAnyJsonFile(Reader().extractorFilePathFromAlbertConfigFiles(
                'config/albert.json'), _readMapJsonFile)
            _extractPath = self.searchScriptNicknameExtractor(searchNickName)
            if not os.path.exists(_extractPath):
                sys.exit(0)
        self.checkForDuppInNicknames()
        return _extractPath

    # ------- # Methods -> searchScriptNickname # ------- #
    def searchScriptNicknameExtractor(self, searchNickName: str):
        # init basic var
        _readMapJsonFile = Reader().readAlbertConfigFiles()
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

