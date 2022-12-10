#!/usr/bin/python3
import datetime
import os
import sys
import argparse

sys.path.insert(1, r'/net/inx971.iil.intel.com/data/tools/FVL_SV_RA/scripts/con/core/scripts/')
# from _crawler import Crawler
# from _logger import logger
# from _readJson import ReadJson
# # ------- # Outside Variable - visual && usefull variable # ------- #
# class ArgumentParserError(Exception): pass
# class ThrowingArgumentParser(argparse.ArgumentParser):
#     def error(self, message):
#         raise ArgumentParserError(message)
# readJsonDataFromMappingFile = ReadJson().readPathLocationFromMap()
# startTime = datetime.datetime.now()
# dashLine = '-------------------------------------------'
# currentSite = 'site_0'
# try:
#     _logger = logger(
#         saveLoggerTypeBool=True,
#         homePathBaseTypeStr=readJsonDataFromMappingFile[currentSite]['systemPath']['homePath'],
#         superUserTypeStr=readJsonDataFromMappingFile[currentSite]['systemPath']['superUser']
#         ,pathToSaveLog=False)
# except (FileNotFoundError,TypeError,KeyError):
#     _logger = logger(saveLoggerTypeBool=True,homePathBaseTypeStr='EMPTY',superUserTypeStr='EMPTY',pathToSaveLog=False)
# # ------- # Outside function - schangeTerminalName # ------- #
# def changeTerminalName():
#     _setNewWindowName = ' '.join(sys.argv[1::])
#     os.system(f'wmctrl -r :ACTIVE: -N "con command --> con {_setNewWindowName}"')
# # ------- # Outside Dynamic Variable - scipt args # ------- #
# scriptName = os.path.basename(__file__)
# pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
# pathScript = os.path.join(pathScriptFolder, scriptName)
# _logger.printLog(0,f'Con was execute on host [{os.uname()[1]}]')
# if __name__ == "__main__":
#     try:
#         # init basic var
#         _searchTypeForArgs = 'public'
#         _sysArgv = sys.argv
#         _runAsSudo = False
#         _scriptCaller = ''
#         _scriptArguemnts = ''
#         _readCrwlerDataTypeDict = True
#         _scriptPathFromCrwler = ''
#         _fullCrwlerCommandToExec = ''
#         # check if sudo is needed
#         if 'sudo' in _sysArgv[1]:
#             _runAsSudo = 'sudo'
#             _scriptCaller = str(_sysArgv[2]).strip()
#             _scriptArguemnts = ' '.join(_sysArgv[3:])
#         if 'sudo' not in _sysArgv[1]:
#             _runAsSudo = ''
#             _scriptCaller = str(_sysArgv[1]).strip()
#             _scriptArguemnts = ' '.join(_sysArgv[2:])
#         # extract script path
#         if _scriptCaller == '-h':
#             pass
#         else:
#             _runAsSudo = 'sudo' 
#             # call the script via os.system
#             _scriptPathFromCrwler = Crawler().recallScriptsPath(
#                 scriptNickNameTypeStr=_scriptCaller,
#                 searchByPrivateOrPublicTypeStr=_searchTypeForArgs)
#             # check if caller is found the item
#             if _scriptPathFromCrwler:
#                 if os.path.basename(_scriptPathFromCrwler) == 'initCommands.py':
#                     if '-cts' in _scriptArguemnts:
#                         _scriptArguemnts = str(_scriptArguemnts).split(' ')
#                         _indexForMatchItem = _scriptArguemnts.index('-cts')+1
#                         _newArgumentsForInitCommand = f"'{' '.join(_scriptArguemnts[_indexForMatchItem::])}'"
#                         _scriptArguemnts = ' '.join(_scriptArguemnts[:_indexForMatchItem])+' '+_newArgumentsForInitCommand
#                     _fullCrwlerCommandToExec = f'{str(_runAsSudo).strip()} python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)
                
#                 elif os.path.basename(_scriptPathFromCrwler) == 'terminalManager.py':
#                     _fullCrwlerCommandToExec = f'python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)  
                
#                 elif os.path.basename(_scriptPathFromCrwler) == 'repoChecking.py':
#                     _fullCrwlerCommandToExec = f'python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)  
                
#                 elif os.path.basename(_scriptPathFromCrwler) == 'autoCompile.py':
#                     _fullCrwlerCommandToExec = f'python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)  
                
#                 elif os.path.basename(_scriptPathFromCrwler) == 'poc.py':
#                     _fullCrwlerCommandToExec = f'python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)  

#                 elif os.path.basename(_scriptPathFromCrwler) == 'pipeline.py':
#                     _fullCrwlerCommandToExec = f'python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)  
                    
#                 elif os.path.basename(_scriptPathFromCrwler) == 'commandRunner.py':
#                     _fullCrwlerCommandToExec = f'python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)  
                
#                 elif os.path.basename(_scriptPathFromCrwler) == 'downloadArtifact.py':
#                     _fullCrwlerCommandToExec = f'python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)  
#                 else:
#                     _fullCrwlerCommandToExec = f'{str(_runAsSudo).strip()} python3 {_scriptPathFromCrwler} {_scriptArguemnts}'.strip()
#                     _logger.printLog(0,f'init remote script [{os.path.basename(_scriptPathFromCrwler)}] | via  script nickname [{_scriptCaller}] | insert args [{_scriptArguemnts}]')
#                     _logger.printLogFinalStatus()
#                     # changeTerminalName()
#                     os.system(_fullCrwlerCommandToExec)
#                     exit(0)

#         try:
#             # show possible args
#             _pathForCon = readJsonDataFromMappingFile['pathConScript']
#             _exampleText = f"""
#  {dashLine*2}
#  Quick deploy con on new host : 
#  \tpython3 {_pathForCon} -deploy_con
#  {dashLine*2}
#  """
#             args = Crawler().configParser(
#                 searchByPrivateOrPublicOrBothTypeStr=_searchTypeForArgs,
#                 initReadMapJsonFileTypeBoolOrDict=_readCrwlerDataTypeDict,
#                 exampleToHowToRunScriptTypeBool=_exampleText).parse_args()

#         except :
#             pass
#     except IndexError:
#         pass

# #  ################# How to use the Script name --> -command ################# 
# #   Possible option to create commands patterns :
# #  \t{dashLine*2}
# #  \t 1. read all commands values for default user : 
# #         \t 1. con -command -cr
# #  \t{dashLine*2}
# #  \t 2. read spesific command value for default user : 
# #         \t 1. con -command -cr -cn <CommandName>
# #  \t{dashLine*2}
# #  \t 3. execute spesific command for default user : 
# #         \t 1. con -command -ce -cn <CommandName>
# #  \t{dashLine*2}
# #  \t 4. read spesific command value for dynamic user : 
# #         \t 1. con -command -cur -un <UserName> -cn <CommandName>
# #  \t{dashLine*2}
# #  \t 5. execute spesific command for dynamic user : 
# #         \t 1. con -command -cue -un <UserName> -cn <CommandName>
# #  \t{dashLine*2}
# #  \t 6. open the user json file : 
# #         \t 1. con -command -cuw -un <UserName>
# #  {dashLine*2}
# #  ################# How to use the Script name --> -fcrw ################# 
# #   Possible option to create commands patterns :
# #  \t{dashLine*2}
# #    \t 1. Search These values --> Pass && Failed && Error inside /home/sv10g/test1 folder and activated deep search: 
# #     \t\t- con -fcrw -path /home/sv10g/test1 -search Pass Failed Error -ds
# #  \t{dashLine*2}
# #  \t 2. Search These values --> test 1 && test 2 && test 12 and test 1 inside /home/sv10g/test1 folder and activated deep search: 
# #     \t\t- con -fcrw -path /home/sv10g/test1 -search test..1 test..2 test..12..and..test..1 -ds
# #  \t{dashLine*2}
# #  \t 3. Search These values --> test 1 inside /home/sv10g/test1 folder: 
# #     \t\t- con -fcrw -path /home/sv10g/test1 -search test..1  
# #  \t{dashLine*2}
# #  \t 4. Search These values --> test 1 inside X folder and outpout in /home/sv10g/test2 folder: 
# #     \t\t- con -fcrw -path /home/sv10g/test1 -search test..1 -o /home/sv10g/test2
# #  {dashLine*2}
# #  ################# How to use the Script name --> -ard ################# 
# #   Possible option to create commands patterns :
# #    \t 1. Download ci [13848] and check that this ci have files with name [imc.tgz] and [imc.tgz] that the type is [hw] and revstion is [b0]: 
# #     \t\t- I want to download these files : 
# #         \t\t- mev-hw-b0-ci-trunk.13848-imc.tgz  
# #         \t\t- mev-hw-b0-ci-trunk.13848-mev.tgz  
# #         \t1. con -ard -url ubit-artifactory-or.intel.com/artifactory/list/mountevans_sw_bsp-or-local/builds/official/mev-trunk/ci/mev-trunk-ci-13848/deploy/ -rev b0 -ft hw -unpack -com acc.tgz imc.tgz 
# #  \t{dashLine*2}
# #  \t 2. Download ci [13848] and check that this ci have files with name [fedora30.tgz] and [imc-pkgs.tgz ] that the type is [simics] and revstion is [c0]: 
# #     \t\t- I want to download these files : 
# #         \t\t- mev-simics-c0-ci-trunk.13848-fedora30.tgz  
# #         \t\t- mev-simics-c0-ci-trunk.13848-imc-pkgs.tgz 
# #         \t1. con -ard -url ubit-artifactory-or.intel.com/artifactory/list/mountevans_sw_bsp-or-local/builds/official/mev-trunk/ci/mev-trunk-ci-13848/deploy/ -rev c0 -ft simics -unpack -com imc-pkgs.tgz fedora30.tgz 
# #  \t{dashLine*2}
# #  ################# How to use the Script name --> -init_command ################# 
# #   Possible option to create commands patterns :
# #  \t{dashLine*2}
# #  \t 1. Enable ping mode : 
# #         \t 1. con -init_command -mp -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig'
# #  \t{dashLine*2}
# #  \t 2. Enable ping and enumeartion mode : 
# #         \t 1. con -init_command -me -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig'
# #  \t{dashLine*2}
# #  \t 3. Set diffrent timeout to session: 
# #         \t 1. con init_command -timeout 600 -me -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig'
# #  \t{dashLine*2}
# #  \t 4. Save con current Log: 
# #         \t 1. con init_command -save_log /home/sv10g/test1 -timeout 600 -me -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig'
# #  \t{dashLine*2}
# #  \t 5. Activated for loop: 
# #     \t\t- I want to itrate for 5 times this command - mode enumeartion
# #         \t\t 1. con init_command -for 5 -me -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig'
# #         \t\t{dashLine*2}
# #     \t\t- I want to itrate for 5 times this command - mode ping
# #         \t\t 1. con init_command -for 5 -mp -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig'
# #  \t{dashLine*2}
# #  \t 6. deploy command on end with for loop: 
# #     \t\t- After the command is sended I want to send command like [poc/load driver] to host  - mode enumeation
# #         \t\t 1. con init_command -for 5 -me -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig' -on_end 'sudo reboot' 
# #         \t\t{dashLine*2}
# #     \t\t- After the command is sended I want to send command like [poc/load driver] to host  - mode ping
# #         \t\t 1. con init_command -for 5 -me -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig' -on_end 'sudo reboot' 
# #  \t{dashLine*2}
# #  \t 7. deploy command on end with for loop and ping mode and save log to folder: 
# #         \t\t 1. con init_command -save_log /home/sv10g/test1 -timeout 600 -for 5 -me -ni '1.1.1.1' 'ladh1234' -cts 'hostname ; ifconfig' -on_end 'sudo reboot' 
# #  \t{dashLine*2}
# #  ###################################################################################################################  
# #  # Con have more options to run his scripts then what he show here , just enter the script and -h after to see all #
# #  ###################################################################################################################