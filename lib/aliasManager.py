#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch
@Auther Email - bar.rose65@gmail.com

<SCRIPT EXAPLAIN>
"""
import os
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
                        help="attach the name to the alias name - how the alias will call", type=str, default=True)
    parser.add_argument("-value", "--alias_value",
                        help="what happend after the alias will called ?", nargs='+', default=False)
    parser.add_argument("-inject", "--inject",
                        help="inject the new alias to the bash", action='store_true', default=False)
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
            2: "/Users/"  # mac
        }
        if item == '.bash_profile':
            pass
        else:
            _extractUsers = Utils().extractAllUsernamesInCurrentMachine()
            if _extractUsers:
                results = [os.path.join(
                    f'{mapHomeDirName[osSystemType]}{i}', str(item)) for i in _extractUsers]
            return results
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

    # ------- # global function -> injectNewAlias # ------- #
    def injectNewAlias(self,
                       aliasNameToAddTypeStr: str = False,
                       aliasValueToAddTypeStr: str = False):
        # init basic var
        aliasSynatx = ''
        tempListForHoldDataTypeList = []
        fileNameToRewrite = ['.bashrc', '.bash_profile']
        pathBashProfile = list(
            map(self.returnBashProfileFiles, fileNameToRewrite))[0]
        _res = False
        aliasSynatx = self.aliasSyntaxBuilder(
            aliasNameToAddTypeStr, aliasValueToAddTypeStr)
        if not aliasSynatx:
            log.printLog(2, 'Cannot identify alias syntax')
            sys.exit(0)

        # open['.bashrc', '.bash_profile'] and check if alias is not there.
        for eachItem in pathBashProfile:
            if eachItem:
                try:
                    with open(eachItem, 'r') as readBashProfile:
                        for eachRow in readBashProfile.readlines():
                            # get rid of the '\n' for each row
                            eachRowWithoutNewLineError = eachRow.replace(
                                '\n', '')
                            tempListForHoldDataTypeList.append(
                                eachRowWithoutNewLineError)
                    # check if giving item is in the file
                    if aliasSynatx not in tempListForHoldDataTypeList:
                        tempListForHoldDataTypeList.append(aliasSynatx)

                    # write
                    with open(eachItem, 'w') as writeNewDataToBashProfile:
                        for eachRow in tempListForHoldDataTypeList:
                            writeNewDataToBashProfile.write(f'{eachRow}\n')
                    # source
                    os.system(f'source {eachItem}')
                    # clear old data
                    tempListForHoldDataTypeList.clear()
                    _res = True
                except FileNotFoundError as e:
                    log.printLog(
                        2, f'Cannot find [{e}] - go to next bashrc file')
        if _res:
            log.printLog(
                1, f'Succesfully write alias name [{aliasNameToAddTypeStr}] in paths [{pathBashProfile}]')
        return _res


if __name__ == "__main__":

    # alb -alias -name calb -value cd /Users/barhaymovich/tools/dev/albert -inject
    # alb -alias -name calb -value cd /Users/barhaymovich/tools/dev/albert

    args = configParser().parse_args()
    argsWrapper = [args.alias_name, " ".join(args.alias_value)]
#     # ------- # Arguments -> -dac -> deploy_alias_con # ------- #
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
