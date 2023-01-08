#!/usr/bin/python3
import datetime
import os
import argparse
import sys
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(pathScriptFolder, 'lib'))
from logger import logger
from reader import Reader
from crawler import Crawler
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-alb'
# ------- # Outside Variable - visual && usefull variable # ------- #
class ArgumentParserError(Exception):
    pass
class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)
startTime = datetime.datetime.now()
dashLine = '-------------------------------------------'
log = logger(False)

# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
log.printLog(0, f'Albert was execute on host [{os.uname()[1]}]')

if __name__ == "__main__":
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
    except IndexError:
        pass
