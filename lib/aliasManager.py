import os
import argparse
from logger import logger
from reader import Reader
from utils import Utils
import sys
import datetime
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-alias' 
# ------- # Outside Variable - visual && usefull variable # ------- #
readJsonDataFromMappingFile = Reader().readAlbertConfigFiles()
osSystemType = Utils().checkOsPlatform()
log = logger(False)
if osSystemType == 3 or osSystemType == 4:
    log.printLog(2,'Please make sure you on Linux/Mac os - alias cannot work on Windows / diffrent OS.')
    sys.exit(0)
# ------- # Outside function - configParser # ------- #
def configParser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-dac", "--deploy_alias_con", help="deploy alias con on wanted hosts",action='store_true',default=True)
    parser.add_argument("-dacm", "--deploy_alias_con_machine", help="deploy alias con on wanted hosts from the machine bot",action='store_true',default=False)
    return parser
# ------- # global -> outside variable # ------- #
scriptName = os.path.basename(__file__)
# ------- # global function -> returnBashProfileFiles # ------- #
def returnBashProfileFiles(item):
    """Use the creds username for extract which """

    results = []
    if item == '.bash_profile':
        pass
    else:
        _extractUsers = Utils().extractAllUsernamesInCurrentMachine()
        if _extractUsers:
            results = [os.path.join(f'/home/{i}', str(item)) for i in _extractUsers]



        return results
print(returnBashProfileFiles('123'))
exit(0)
# ------- # global function -> checkOsSystem # ------- #
def extractTheRightSyntaxForAdamAutoAlias(aliasNameTypeStr: str, aliasValueTypeStr: str):
    """
    - Explain :
        - Check if the alias value is folder or file:
            - If folder --> add auto c_ before the alias name
            - Else -->
                - add auto f_ before the alias name
    """
    # init basic var
    _aliasName = str(aliasNameTypeStr)
    _aliasValue = str(aliasValueTypeStr)
    _fullAliasName2ndValue = ''
    _aliasHolderTypeList = []
    # check if the alias value is folder
    if os.path.isdir(_aliasValue):
        # ADD C_ BEFORE
        _rawAliasName = _aliasName.replace(".","").strip()
        _aliasName = str(f'c{_rawAliasName}')
        _aliasValue = f'cd {_aliasValue}'
        _fullAliasName2ndValue = f"alias {_aliasName}='{_aliasValue}'"
        _aliasHolderTypeList.append(_fullAliasName2ndValue.strip())
    # check if the alias value is file
    else:
        _rawAliasName = _aliasName.replace(".","").strip()
        _aliasName = str(f'{_rawAliasName}')
        # check if alias is finish with .py
        if '.pyc' not in _aliasValue and '.py' in _aliasValue:
            _aliasValue = f'python3 {_aliasValue}'
            # ragulaer
            _fullAliasName2ndValue = f"alias {_aliasName}='{_aliasValue}'"
            _aliasHolderTypeList.append(_fullAliasName2ndValue.strip())
            # sudo
            _fullAliasName2ndValue = f"alias sudo_{_aliasName}='sudo {_aliasValue}'"
            _aliasHolderTypeList.append(_fullAliasName2ndValue.strip())  
    # return
    return _aliasHolderTypeList


# read and modify bash profile file
def readAndModifyBashProfileFile(
        aliasNameToAddTypeStr: str = False,
        aliasValueToAddTypeStr: str = False):
    # init basic var
    counter = 1
    aliasSynatx = ''
    tempListForHoldDataTypeList = []
    fileNameToRewrite = ['.bashrc', '.bash_profile']
    pathBashProfile = list(map(returnBashProfileFiles, fileNameToRewrite))[0]
    if aliasNameToAddTypeStr and aliasValueToAddTypeStr:
        _hostname = os.uname()[1]
        log.printLog(0,f'Start deploy con on host [{_hostname}]')
        aliasSynatx = extractTheRightSyntaxForAdamAutoAlias(
            aliasNameToAddTypeStr, aliasValueToAddTypeStr)
    # print
    counter += 1
    # open the bash_profile and update it to adam -- read
    for eachItem in pathBashProfile:
        if eachItem == None:
            pass
        else:
            try:
                with open(eachItem, 'r') as readBashProfile:
                    for eachRow in readBashProfile.readlines():
                        # get rid of the '\n' for each row
                        eachRowWithoutNewLineError = eachRow.replace('\n', '')
                        tempListForHoldDataTypeList.append(eachRowWithoutNewLineError)
                # check if giving item is in the file
                for eachAlias in sorted(aliasSynatx):
                    if eachAlias not in tempListForHoldDataTypeList:
                        tempListForHoldDataTypeList.append(eachAlias)

                # write
                counter += 1
                with open(eachItem, 'w') as writeNewDataToBashProfile:
                    for eachRow in tempListForHoldDataTypeList:
                        writeNewDataToBashProfile.write(f'{eachRow}\n')
                # source
                os.system(f'source {eachItem}')
                # clear old data

                tempListForHoldDataTypeList.clear()
            except FileNotFoundError as e:
                log.printLog(2,f'Cannot find [{e}] - go to next bashrc file')
    log.printLog(1,f'con was succsfully deploy.')
    log.printLog(0,f'Please re-open terminal and insert [con -h] to check avaliable methods.')

if __name__ == "__main__":


    args = configParser().parse_args()
    # ------- # Arguments -> -dac -> deploy_alias_con # ------- #
    
    if args.deploy_alias_con_machine:
        Switz().checkLib()
        log.printLog(0,'deploy from machine bot')
        os.system('source /net/inx971.iil.intel.com/data/tools/sv_setup.sh -project MEV')
        readAndModifyBashProfileFile('con',readJsonDataFromMappingFile['pathConScript'])
    else:
        Switz().checkLib()
        os.system('source /net/inx971.iil.intel.com/data/tools/sv_setup.sh -project MEV')
        readAndModifyBashProfileFile('con',readJsonDataFromMappingFile['pathConScript'])
