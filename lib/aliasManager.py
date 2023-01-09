#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch
@Auther Email - bar.rose65@gmail.com

<SCRIPT EXAPLAIN>
"""
import os
import subprocess
import argparse
from logger import logger
from reader import Reader
from utils import Utils
import sys
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-alias'
# ------- # Outside Variable - visual && usefull variable # ------- #
readJsonDataFromMappingFile = Reader().readAlbertConfigFiles()
osSystemType = Utils().checkOsPlatform()
log = logger(False)
if osSystemType == 3 or osSystemType == 4:
    log.printLog(
        2, 'Please make sure you on Linux/Mac os - alias cannot work on Windows / diffrent OS.')
    sys.exit(0)
    
# ------- # Outside function - configParser # ------- #
def configParser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-name", "--alias_name",
                        help="attach the name to the alias name - how the alias will call", type=str, default=False)
    parser.add_argument("-value", "--alias_value",
                        help="what happend after the alias will called ?", nargs='+', default=False)
    parser.add_argument("-inject", "--inject",
                        help="inject the new alias to the bash", action='store_true', default=False)
    parser.add_argument("-inject_albert", "--inject_albert",
                        help="inject albert into system", action='store_true', default=False)
    return parser

# ------- # global -> outside variable # ------- #
scriptName = os.path.basename(__file__)

# ------- # Class -> AliasManager # ------- #
class AliasManager():
    """
    - Exaplain :
        - Example this tamplate class
    """

    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #

    # ------- # global function -> returnBashProfileFiles # ------- #
    def returnBashProfileFiles(self, item):
        """Use the creds username for extract which """
        results = []
        mapHomeDirName = {
            1: "/home/",  # linux
            2: "/Users/",  # mac,
            3: "/root/"  # for root
        }
        if item == '.bash_profile':
            pass
        else:
            _extractUsers = Utils().extractAllUsernamesInCurrentMachine()
            if _extractUsers:
                results = [os.path.join(
                    f'{mapHomeDirName[osSystemType]}{i}', str(item)) for i in _extractUsers]
                results = [i.replace(
                    '/home/root/', "/root/").replace("/Users/root/", "/root/") for i in results]
        return results
    
    # ------- # method -> injectAlbertAlias # ------- #
    def injectAlbertAlias(self):
        log.printLog(0, 'Start update albert alias')
        _mapper = {
            'alb': Reader().extractorFilePathFromAlbertConfigFiles('albert/albert.py'),
            'albert': Reader().extractorFilePathFromAlbertConfigFiles('albert/albert.py'),
        }
        for aliasName, aliasVal in _mapper.items():
            self.injectNewAlias(aliasName, aliasVal)
        self.injectNewAlias('calb',f'cd {Reader().extractorFilePathFromAlbertConfigFiles("albert")}')
            
    # ------- # global function -> checkOsSystem # ------- #
    def aliasSyntaxBuilder(self, aliasNameTypeStr: str, aliasValueTypeStr: str):
        """
        check if alias name and value is giving && return builder
        """
        # init basic var
        _aliasName = str(aliasNameTypeStr).strip()
        _aliasValue = str(aliasValueTypeStr).strip()
        _aliasBuilder = False
        if len(_aliasName) > 0 and len(_aliasValue) > 0:
            _aliasBuilder = f"alias {_aliasName}='{_aliasValue}'"
        return _aliasBuilder

    # ------- # global function -> checkExistsAlias # ------- #
    def checkExistsAlias(self, bashrcPath: str, aliasSyntx: str):
        """
        Check if alias is exsits , return True/False
        """
        _commnad = f'cat {bashrcPath} | grep "{aliasSyntx}"'
        _checkAlias = Utils().deployCommandSubprocess(_commnad, enablePrint=False)
        _res = False
        if _checkAlias:
            _res = True

        return _res

    # ------- # global function -> injectAlbertIntoPathVar # ------- #
    def injectAlbertIntoPathVar(self):
        # init basic vars
        _paths = ['/usr/local/bin']
        _status = False
        
        for _ in _paths:
            if os.path.exists(_):
                if 'albert.py' in os.listdir(_):
                    _status = True
                    break
                else:
                    _createLinkCommand = f'sudo ln -s {Reader().extractorFilePathFromAlbertConfigFiles("albert.py")} {_}'
                    # print(_createLinkCommand)
                    log.printLog(0,f'Create new sym into path [{_}]')
                    os.system(_createLinkCommand)
                    _status = True
        if _status:
            log.printLog(1,'Succsfully inject albert.py into $PATH folder var')
        else:
            log.printLog(2,f'Cannot inject albert.py into $PATH , please make sure these path are exists [{_paths}]')
        return _status
        
    # ------- # global function -> injectNewAlias # ------- #
    def injectNewAlias(self,
                       aliasNameToAddTypeStr: str = False,
                       aliasValueToAddTypeStr: str = False):
        # init basic var
        aliasSynatx = ''
        fileNameToRewrite = ['.bashrc', '.bash_profile','.zshrc']
        _pathBashProfile = list(
            map(self.returnBashProfileFiles, fileNameToRewrite))
        pathBashProfile = set()
        for _ in _pathBashProfile:
            if _:
                for _eachElem in _:
                    pathBashProfile.add(_eachElem)
        _res = False
        aliasSynatx = self.aliasSyntaxBuilder(
            aliasNameToAddTypeStr, aliasValueToAddTypeStr)

        if not aliasSynatx:
            log.printLog(2, 'Cannot identify alias syntax')
            sys.exit(0)

        # open['.bashrc', '.bash_profile'] and check if alias is not there.
        for eachItem in pathBashProfile:
            if eachItem and os.path.exists(eachItem):
                try:

                    _checkAlias = self.checkExistsAlias(eachItem,aliasSynatx)
                    if not _checkAlias:
                        log.printLog(
                            9, f'Start install alias [{aliasNameToAddTypeStr}] into [{eachItem}]')
                        _command = f'sudo echo "{aliasSynatx}" >> {eachItem}'
                        os.system(_command)
                        # recheck
                        _checkAlias = self.checkExistsAlias(eachItem,aliasSynatx)
                        if not _checkAlias:
                            log.printLog(
                                2, f'Seems like there been an error with try to install alias [{aliasSynatx}] into [{eachItem}]')
                        else:
                            log.printLog(
                                1, f'Succesfully write alias name [{aliasNameToAddTypeStr}] in paths [{pathBashProfile}]')

                    else:
                        log.printLog(
                            1, f'Succesfully write alias name [{aliasNameToAddTypeStr}] in paths [{pathBashProfile}]')

                    # source
                    # print(f'source {eachItem}')
                    # (f'source {eachItem}')

                except FileNotFoundError as e:
                    log.printLog(
                        2, f'Cannot find [{e}] - go to next bashrc file')

        return _res


if __name__ == "__main__":

    # alb -alias -name calb -value cd /Users/barhaymovich/tools/dev/albert -inject
    # alb -alias -name calb -value cd /Users/barhaymovich/tools/dev/albert

    args = configParser().parse_args()
    argsWrapper = [args.alias_name, " ".join(
        args.alias_value) if args.alias_value else False]
    # ------- # Arguments -> -dac -> deploy_alias_con # ------- #
    if argsWrapper[0] and argsWrapper[1]:
        _aliasBuilder = AliasManager().aliasSyntaxBuilder(
            argsWrapper[0], argsWrapper[1])
        if args.inject:
            log.printLog(
                0, f'Start to inject alias [{_aliasBuilder}] to bash.')
            AliasManager().injectNewAlias(argsWrapper[0], argsWrapper[1])
        else:
            print(AliasManager().aliasSyntaxBuilder(
                argsWrapper[0], argsWrapper[1]))
    # ------- # Arguments -> -dac -> deploy_alias_con # ------- #
    elif args.inject_albert:
        AliasManager().injectAlbertAlias()
        AliasManager().injectNewAlias('calb',f'cd {Reader().extractorFilePathFromAlbertConfigFiles("albert")}')