#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch
@Auther Email - bar.rose65@gmail.com
<SCRIPT EXAPLAIN>
create user command for improve workflow
------------
alb -pipe -show
alb -pipe -example
"""
import argparse
import time
import os
import datetime
import configparser
from logger import logger
from reader import Reader

import sys
from utils import Utils

# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-pipe'
# ------- # Outside Variable - visual && usefull variable # ------- #
scriptRandomNumber = Utils().randomNumber()
getCurrnetHostname = Utils().getHostname()
currentData = Utils().getAutoTime(returnOnlyDate=True,
                                  returnDataAndTimeNoMilsec=False, returnDateAndTime=False)


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


startTime = datetime.datetime.now()
dashLine = '-------------------------------------------'
confObject = configparser.ConfigParser()
log = logger(False)
# # ------- # Try - Import paramiko # ------- #
# Utils().checkLib()
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
deployScriptAsSudo = f'sudo python3 {pathScript}'

# ------- # Outside function - configParser # ------- #


def configParser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-example", "--example", help="Run to show example ",
                        action='store_true', required=False, default='Default')
    # must
    parser.add_argument("-u", "--user", help="run on which user ? ",
                        type=str, required=False, default='Default')
    parser.add_argument(
        "-p", "--pipe_name", help="how the pipeline name will call ?", required=False, default=False)
    # option to exec
    parser.add_argument("-r", "--read", help="read the command",
                        required=False, action='store_true', default=False)
    parser.add_argument("-show", "--show", help="show user pipeline",
                        required=False, action='store_true', default=False)
    parser.add_argument("-w", "--write", help="write the command",
                        required=False, action='store_true', default=False)
    parser.add_argument("-e", "--exec", help="exec the command",
                        required=False, action='store_true', default=False)
    parser.add_argument("-a", "--arguments", help="exec the command",
                        required=False, nargs='+', default=False)
    parser.add_argument("-d", "--description", help="show desription inside the pipe",
                        required=False, action='store_true', default=False)
    # section option
    parser.add_argument("-sr", "--section_run", help="pick which section to you want to run",
                        choices=['pre', 'run', 'post'], nargs='+', required=False, default=['pre', 'run', 'post'])

    parser.add_argument("-dat", "--deploy_auto_tamplate", help=argparse.SUPPRESS,
                        required=False, action='store_true', default=False)

    return parser
# ------- # Methods -> pipeReaderForUsers # ------- #


def selfLogging(
    pipeUser: str,
    pipeName: str,
    section: str,
    itrationStart: int,
    totalItration: int,
    commandRunning: str,
    startOrEndCommand: str
):
    """
    Write data to local files with all data what happend in the pipe.
    """
    # inti basic vars
    _pathFolderLoggingData = os.path.join(os.path.expanduser(
        "~"), 'pipeline_logging_data', f'pipeUser_{pipeUser}', f'pipeName_{pipeName}', f'PipeId_{scriptRandomNumber}')
    _pathFileLoggingData = os.path.join(
        _pathFolderLoggingData, 'pipeline_logging.txt')
    _data = []
    if not os.path.exists(_pathFolderLoggingData) or not os.path.exists(_pathFileLoggingData):
        os.system(f'sudo mkdir -p {_pathFolderLoggingData}')
        os.system(f'sudo chmod 777 {_pathFolderLoggingData}')
        # log.printLog(0,f'Logging data is going to save on this folder [{_pathFileLoggingData}]')
        _data.append(
            f'Start capture pipe  - Pipe name {pipeName} | Pipe user {pipeUser}.')
        _data.append(f'Run From host [{Utils().getHostname()}]')
        # _data.append(f'{str(datetime.datetime.now())} [{section} - {itrationStart}/{totalItration}] {startOrEndCommand} Running command -> {commandRunning}')
        _data.append(
            f'{str(datetime.datetime.now())} [{section} - {itrationStart}/{totalItration}] Running command -> {commandRunning}')
        with open(_pathFileLoggingData, 'w') as writeNewPipeLogs:
            for _eachItem in _data:
                writeNewPipeLogs.write(_eachItem+'\n')
    else:
        with open(_pathFileLoggingData, 'a') as updatePipeLogs:
            # _data.append(f'{str(datetime.datetime.now())} [{section} - {itrationStart}/{totalItration}] {startOrEndCommand} Running command -> {commandRunning}')
            _data.append(
                f'{str(datetime.datetime.now())} [{section} - {itrationStart}/{totalItration}] Running command -> {commandRunning}')
            for _eachItem in _data:
                updatePipeLogs.write(_eachItem+'\n')
# ------- # Class -> Pipeline # ------- #


class Pipeline():
    """
    - Exaplain :
        - Example this tamplate class
    """

    def __init__(
        self,
        pipelineName: str,
        username: str = 'default',
    ):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        self.nameUser = username.strip()
        self.pipeName = pipelineName.strip()
        self.nameFileExtation = '.ini'
        # ------- # Default attributes -> Path # ------- #
        self.pathFolderUsersCommandExec = Reader(
        ).extractorFilePathFromAlbertConfigFiles('pipe')
        self.pathFolderUserCommandExec = os.path.join(
            self.pathFolderUsersCommandExec, f'username_{self.nameUser}')
        self.pathFileCommandUser = os.path.join(
            self.pathFolderUserCommandExec, f'pipeline_{self.pipeName}_{self.nameFileExtation}')

        if not os.path.exists(self.pathFolderUserCommandExec):
            os.system(f'sudo mkdir -p {self.pathFolderUserCommandExec}')

    # ------- # Methods -> addSection # ------- #
    def addSection(self, confObject: object, sectionName: str, sectionData: dict):
        # init basic vars
        _confObject = confObject
        _sectionName = str(sectionName).strip().capitalize()
        # ADD SECTION
        _confObject.add_section(_sectionName)
        # ADD SETTINGS TO SECTION
        for k, v in sectionData.items():
            k, v = str(k).strip(), str(v).strip()
            _confObject.set(_sectionName, k, v)

        return _confObject

    # ------- # Methods -> createNewPipeline # ------- #
    def createNewPipeline(self, confObject: object, locationToPut: str):
        # SAVE CONFIG FILE
        with open(self.pathFileCommandUser, 'w') as newCommand:
            confObject.write(newCommand)
            newCommand.flush()
            newCommand.close()
        os.system(f'sudo chmod -R 777 {self.pathFolderUserCommandExec}')
        log.printLog(1, f'pipeline was created.')

    # ------- # Methods -> createAutoPipelineAutomation # ------- #
    def createAutoPipelineAutomation(self, user: str):
        Utils().spliter()
        log.printLog(
            7, f'wellcome new user [{user.capitalize()}] , create auto pipeline for you.', 'WellcomeMessage', 5)
        Utils().spliter()
        # inti basic vars
        confObject = configparser.ConfigParser()
        confObject = self.addSection(confObject, 'PipelineInfo',
                                     {
                                         "create_for_user": self.nameUser,
                                         "pipe_name": self.pipeName,
                                         "create_timestemp": str(datetime.datetime.now()),
                                         "description": """\n####################### This is basic description #######################\n          - Deploy order and visual pipeline for users\n          - Write basic description for user""",

                                     }
                                     )
        confObject = self.addSection(confObject, 'Vars',
                                     {
                                         "Var_example_1": "echo InsertWhatEverYouWant1",
                                         "Var_example_2": "echo InsertWhatEverYouWant1 you can with spaces",
                                         "Var_example_3": "echo InsertWhatEverYouWant1 and symbols !@3!",
                                     }
                                     )

        confObject = self.addSection(confObject, 'ForLoops',
                                     {
                                         "for_loop_for_pre_section": "1",
                                         "for_loop_for_run_section": "1",
                                         "for_loop_for_post_section": "1",
                                         "for_loop_for_all_sections": "1",
                                     }
                                     )

        confObject = self.addSection(confObject, 'Triggers',
                                     {
                                         "enable": "false",
                                         "run_at_days": "1 2 3 4 5 6 7",
                                         "run_at_times": "07:00:00",
                                     }
                                     )

        confObject = self.addSection(confObject, 'Pre',
                                     {
                                         "1": "echo ^var_example_1 ; echo ^currentDate",
                                         "2": "echo ^current_hostname_lower",
                                         "3": "echo ^current_hostname_upper",
                                     }
                                     )
        confObject = self.addSection(confObject, 'Run',
                                     {
                                         "1": "echo ^var_example_1 ; echo ^currentDate (for:2 sleep:2 on_end:var_example_3)",
                                         "2": "echo ^currentMiliTimeDate",
                                         "3": "echo ^currentTimeDate",
                                     }
                                     )
        confObject = self.addSection(confObject, 'Post',
                                     {
                                         "1": "echo ^var_example_1 ; echo ^currentDateTamplate^currentMiliTimeDateTamplate",
                                         "2": "cd ; pwd",
                                         "2": "ll ; pwd",
                                         "3": "cd ../ ; pwd",
                                     }
                                     )

        self.createNewPipeline(confObject, self.pathFileCommandUser)
        os.system(f'sudo vi {self.pathFileCommandUser}')

    # ------- # Methods -> readPipelineFile # ------- #
    def readPipelineFile(self):
        if not os.path.exists(self.pathFileCommandUser):
            _command = f'{deployScriptAsSudo} {" ".join(sys.argv[1::])} -dat'.replace(
                '-e', '').replace('-w', '').replace('-r', '')
            os.system(_command)
            exit(0)

        _data = {}
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config.read(self.pathFileCommandUser)

        for _each in config.sections():
            if _each not in _data.keys():
                _data[_each] = {}
            for _eachKey, _eachValue in config.items(_each):

                if _each == 'Vars':
                    _data[_each]['^'+_eachKey] = str(_eachValue)
                else:
                    _data[_each][_eachKey] = str(_eachValue)

        return _data

    # ------- # Methods -> extractOptionValue # ------- #
    def extractOptionValue(self, optionString: str):
        """return the option value (option:value) - return str"""
        return optionString.split(':')[1]

    # ------- # Methods -> searchForVars # ------- #
    def searchForVars(self, valueToCheck: str, varsDict: dict):
        """search variable in giving sentence - aka variable - return str"""
        _results = valueToCheck
        # if '^' in _results and [i for i in valueToCheck.split() if i in varsDict['Vars'].keys()]:

        if '^' in _results:
            for _eachKey in varsDict['Vars'].keys():
                _results = str(_results).replace(
                    _eachKey, varsDict['Vars'][_eachKey])
        return _results

    # ------- # Methods -> searchForApendixOptions # ------- #
    def searchForApendixOptions(self, valueToCheck: str, varsDict: dict):
        """search for option in giving sentence - aka variable- return list"""
        _results = []
        if '(' in valueToCheck:
            _dataChecker = " ".join(valueToCheck.split(
                '(')[1::]).strip().replace(')', '').split(' ')
            valueToCheck = " ".join(valueToCheck.split(
                '(')[0:1]).strip().replace(')', '')
            for _eachItem in _dataChecker:
                # for
                if 'for' in _eachItem:
                    _optionValue = self.extractOptionValue(_eachItem)
                    log.printLog(
                        7, f'Deploy apendix [for loop] for total [{_optionValue}] to action [{valueToCheck}]', 'Activated Apendix Option', 1)
                    for _ in range(1, int(_optionValue)+1):
                        _results.append(valueToCheck)
                # sleep
                elif 'sleep' in _eachItem:
                    _optionValue = self.extractOptionValue(_eachItem)
                    log.printLog(
                        7, f'Deploy apendix [sleep time] value to [{_optionValue}] for each action [{valueToCheck}]', 'Activated Apendix Option', 1)

                    if _results:
                        _results = [
                            f'{i} ; sleep {_optionValue}' for i in _results]
                    else:
                        _results = [
                            f'{i} ; sleep {_optionValue}' for i in [valueToCheck]]
                # one end
                elif 'on_end' in _eachItem:
                    _optionValue = f'^{self.extractOptionValue(_eachItem)}'
                    _resultsVars = self.searchForVars(_optionValue, varsDict)
                    if '^' in _resultsVars:
                        log.printLog(
                            2, f'{_resultsVars} not match in vars section - ignoreing')
                    else:
                        log.printLog(
                            7, f'Deploy apendix [on_end time] value to [{_resultsVars}] for each action [{valueToCheck}]', 'Activated Apendix Option', 1)
                        if _results:
                            _results = [
                                f'{i} ; {_resultsVars}' for i in _results]
                        else:
                            _results = [
                                f'{i} ; {_resultsVars}' for i in [valueToCheck]]
                # new terminal
                elif 'new_terminal' in _eachItem:
                    _optionValue = self.extractOptionValue(_eachItem)
                    log.printLog(
                        7, f'Deploy apendix [new terminal] value to [{_optionValue}] for each action [{valueToCheck}]', 'Activated Apendix Option', 1)
                    _results = [
                        f'con -ter -win {valueToCheck.replace(" ","..")}']
        else:
            _results.append(valueToCheck)
        return _results

    # ------- # Methods -> searchForArgeumnts # ------- #
    def searchForArgeumnts(self, valueToCheck: str, argeumntsToFetch: dict):
        # print(argeumntsToFetch,valueToCheck)
        _argeumntsToFetch = argeumntsToFetch
        _results = valueToCheck
        _totalArgsInWord = set()
        _searcher = ['?'+str(i) for i in list(range(1, 101))]
        for n, _eachSearcher in enumerate(_searcher):
            if _eachSearcher in valueToCheck:
                _totalArgsInWord.add(_eachSearcher)

        if _totalArgsInWord:
            if len(_totalArgsInWord) > len(argeumntsToFetch.keys()):
                _missing = max(len(_totalArgsInWord),len(argeumntsToFetch.keys())) - min(len(_totalArgsInWord),len(argeumntsToFetch.keys()))
                log.printLog(
                    2, f'Cannot procced with pipe - missing [{_missing}] args - possible args {list(_totalArgsInWord)}')
                exit(0)
        if bool(_argeumntsToFetch) == False and '?' in valueToCheck:
            log.printLog(
                2, 'Please note that you insert argeumnt to the script without calling them , cannot countiue with the script.')
            exit(0)
        else:
            while '?' in _results:
                for _eachKey in argeumntsToFetch.keys():
                    _results = str(_results).replace(
                        str(_eachKey).strip(), argeumntsToFetch[_eachKey])

        if '?' in _results:
            log.printLog(
                2, 'Please note that you insert argeumnt to the script without calling them , cannot countiue with the script.')
            exit(0)
        return _results

    # ------- # Methods -> mapSections # ------- #
    def mapSections(
        self,
        sectionName: str,
        dictToSerach: dict,
        varsDict: dict,
        optionDict: dict,
        argeumntsToFetch: dict,
        terminalManager: dict
    ):
        """map the pre/run/post sections - return dict"""
        # init basic vars

        _resultsDict = {}
        _finalResultsDict = {}
        _results = []
        _matchFinale = 1
        # _enableSetupOptionCheck = optionDict['Setupoptions']['enable']
        _enableSetupOptionCheck = 'false'
        # _enableTerminalManager = terminalManager['TermianlManager'][sectionName]
        _enableTerminalManager = 'false'
        _counter = 1

        for _, _data in dictToSerach.items():
            for _index, _value in _data.items():
                # _index = int(_index)
                _resultsDict[_counter] = self.searchForArgeumnts(
                    self.searchForVars(_value, varsDict), argeumntsToFetch)
                _counter += 1
        for _index, _value in _resultsDict.items():
            _results.append([i for i in self.searchForArgeumnts(
                self.searchForApendixOptions(_value, varsDict), argeumntsToFetch)])

        for _eachItem in _results:
            for _valueFinale in _eachItem:
                # check if the setup option is false
                if _enableSetupOptionCheck == 'false':
                    _finalResultsDict[_matchFinale] = self.searchForArgeumnts(
                        _valueFinale, argeumntsToFetch)
                    _matchFinale += 1
        return _finalResultsDict

    # ------- # Methods -> searchCdInCommand # ------- #
    def searchCdInCommand(self, commandToSearchIn: str, varsDict: dict, argeumntsToFetch: dict):

        _commandToSearchIn = commandToSearchIn.strip()
        _results = False
        if 'cd' == _commandToSearchIn:
            _commandToSearchIn = os.path.expanduser('~')
            self.deployCommand(_commandToSearchIn, varsDict,
                               argeumntsToFetch, True)
            _results = True

        elif 'cd' in _commandToSearchIn:
            for _eachWord in _commandToSearchIn.split(' '):

                if 'cd' == _eachWord:
                    _commandToSearchIn = _commandToSearchIn.replace(
                        'cd', '').strip()
                    self.deployCommand(_commandToSearchIn,
                                       varsDict, argeumntsToFetch, True)
                    _results = True

        return _results

    # ------- # Methods -> deployCommand # ------- #
    def deployCommand(self, commandToDeploy: str, varsDict: dict, argeumntsToFetch: dict, chdir: bool = False):
        _commandToDeploy = commandToDeploy.strip()
        _commandToDeploy = " ".join(
            Utils().searchAlbertInisdeWords(commandToDeploy))
        log.printLog(
            7, f'Command Value -> {_commandToDeploy}', 'Deploy Command', 4)
        if chdir:
            os.chdir(_commandToDeploy)
            log.printLog(
                7, f'Current Path -> {os.getcwd()}', 'Path Location', 0)
        else:
            if 'pwd' == _commandToDeploy:
                log.printLog(
                    7, f'Current Path -> {os.getcwd()}', 'Path Location', 0)
            elif 'll' in [i for i in _commandToDeploy.split()]:
                _commandToDeploy = _commandToDeploy.replace('ll', 'ls -al')
                _commandToDeploy = self.searchForArgeumnts(
                    self.searchForVars(_commandToDeploy, varsDict), argeumntsToFetch)
                os.system(_commandToDeploy)
            elif 'break_point' == _commandToDeploy:
                log.printLog(0, 'Deploy break point in pipe')
                input(log.printLog(7, 'Please insert enter to continue : ', 'Break_Point_Activated',
                      3))
            else:
                _commandToDeploy = self.searchForArgeumnts(
                    self.searchForVars(_commandToDeploy, varsDict), argeumntsToFetch)
                os.system(_commandToDeploy)
    # ------- # Methods -> iterateEachSection # ------- #

    def iterateEachSection(
        self,
        sectionName: str,
        sectionData: dict,
        currentForLoopCounter: int,
        totalForLoopCounter: int,
        abortAtArgeument: dict,
        argeumntsToFetch: list,
        varsDict: dict,
    ):
        # dashLine = "="*20
        # init basic vars
        # print(abortAtArgeument[sectionName])
        _abortAtArgeument = abortAtArgeument
        _abortAtArgeumentEnable = 'false'
        _abortAtArgeumentSection = ''
        _activatedSection = True
        if _abortAtArgeument:
            _abortAtArgeumentEnable = abortAtArgeument['enable']
            _abortAtArgeumentSection = abortAtArgeument[sectionName].split()

        log.printLog(
            7, f'{dashLine} # Start Section -> {sectionName.capitalize()}  | for loop counter [{currentForLoopCounter}/{totalForLoopCounter}] # {dashLine}', 'Section Starting', 1)
        log.printLog(0, f'Start {sectionName} pipeline')
        if _abortAtArgeumentEnable == 'true':

            if not [i for i in _abortAtArgeumentSection if str(i).strip() not in argeumntsToFetch]:
                log.printLog(11, f'Ignore section [{sectionName}]')
                _activatedSection = False
        if _activatedSection:
            for _k, _command in sectionData.items():
                log.printLog(7, f'Start Sub Section [{_k}]', 'Sub Section', 3)

                # Switz().addScriptToStatusManager(
                # scriptNickname=scriptNickname,
                # randomeIdNumber=scriptRandomNumber,
                # sysArgvForActionRunning=sys.argv,
                # username='Default',
                # commandName='Default',
                # runToHost=getCurrnetHostname,
                # iter=str(currentForLoopCounter),
                # totalIter=str(totalForLoopCounter),
                # timeForOpenSesstion=str(startTime)
                # )

                selfLogging(
                    pipeName=self.pipeName,
                    pipeUser=self.nameUser,
                    section=sectionName,
                    itrationStart=currentForLoopCounter,
                    totalItration=totalForLoopCounter,
                    commandRunning=_command,
                    startOrEndCommand='Start')

                # Switz().changeTerminalName(f'con con Pipe Name : [{self.pipeName}] | Pipe User : [{self.nameUser}] | Running section : [{sectionName}] | sub section : [{_k}]'.split(' '))
                if ';' in _command:
                    _command = _command.split(';')
                    for _eachCommandSpliter in _command:
                        _eachCommandSpliter = _eachCommandSpliter.strip()
                        if not self.searchCdInCommand(_eachCommandSpliter, varsDict, argeumntsToFetch):
                            self.deployCommand(
                                _eachCommandSpliter, varsDict, argeumntsToFetch, False)
                else:
                    if not self.searchCdInCommand(_command, varsDict, argeumntsToFetch):
                        self.deployCommand(
                            _command, varsDict, argeumntsToFetch, False)
                        # deployCommand(_command,False)

                # selfLogging(
                #     pipeName=self.pipeName,
                #     pipeUser=self.nameUser,
                #     section=sectionName,
                #     itrationStart=currentForLoopCounter,
                #     totalItration=totalForLoopCounter,
                #     commandRunning=_command,
                #     startOrEndCommand='End  ')
            # Switz().removeScriptToStatusManager(releaseByRunToHost=getCurrnetHostname,randomeIdNumber=scriptRandomNumber)

    # ------- # Methods -> parserAllSections # ------- #
    def parserAllSections(self, argeumntsToFetch: list = False):
        log.printLog(0, 'Start parsing pipeline.')
        _argeumntsToFetch = {}
        if argeumntsToFetch:
            log.printLog(
                0, f'Start mapping arguemnts from user -> total recive args -> [{len(argeumntsToFetch)}]')

            for n, _eachArg in enumerate(argeumntsToFetch, start=1):
                _index = '?'+str(n)
                _argeumntsToFetch[_index] = _eachArg
                log.printLog(
                    0, f'Arguemnt [{_eachArg}] recive name [{_index}]')

        # init basic vars

        _readPipelineFile = self.readPipelineFile()
        _executerDict = {
            'Vars': {},
            'Pre': {},
            'Run': {},
            'Post': {},
            'Setupoptions': {},
            'Forloops': {},
            'Triggers': {},
            'Abortsectionsifarguemntis': {},
            'TermianlManager': {},
            'send_email': {}
        }

        _loopsCounterForSections = []
        _triggersActions = False
        triggerEmail = False
        _preFinal = {}
        _runFinal = {}
        _postFinal = {}
        for _eachKeyForExecuter in _executerDict.keys():

            for _eachKey in _readPipelineFile.keys():
                if _eachKey == _eachKeyForExecuter:
                    _executerDict[_eachKey] = _readPipelineFile[_eachKey]
        # add extract options to variables data
        _executerDict['Vars']['^currentDate'] = Utils().getAutoTime(
            returnDataAndTimeNoMilsec=False,
            returnDateAndTime=False,
            returnOnlyDate=True)+'_'
        _executerDict['Vars']['^currentTimeDate'] = '_'+Utils().getAutoTime(
            returnDataAndTimeNoMilsec=True,
            returnDateAndTime=False,
            returnOnlyDate=False)+'_'
        _executerDict['Vars']['^currentMiliTimeDate'] = '_'+Utils().getAutoTime(
            returnDataAndTimeNoMilsec=False,
            returnDateAndTime=True,
            returnOnlyDate=False)+'_'
        _executerDict['Vars']['^current_hostname_lower'] = str(
            os.uname().nodename).lower()
        _executerDict['Vars']['^current_pipe_name'] = self.pipeName
        _executerDict['Vars']['^current_pipe_user'] = self.nameUser
        _executerDict['Vars']['^current_thread'] = str(os.getpid())
        _executerDict['Vars']['^uniq_Id'] = str(f'{scriptRandomNumber}')

        _preFinal = self.mapSections(
            'pre',
            {"Pre": _executerDict['Pre']},
            {"Vars": _executerDict['Vars']},
            _executerDict['Setupoptions'],
            _argeumntsToFetch,
            _executerDict['TermianlManager'])
        _runFinal = self.mapSections(
            'run',
            {"Run": _executerDict['Run']},
            {"Vars": _executerDict['Vars']},
            _executerDict['Setupoptions'],
            _argeumntsToFetch,
            _executerDict['TermianlManager'])
        _postFinal = self.mapSections(
            'post',
            {"Post": _executerDict['Post']},
            {"Vars": _executerDict['Vars']},
            _executerDict['Setupoptions'],
            _argeumntsToFetch,
            _executerDict['TermianlManager'])

        # add for loop to section
        # [1 2 3 4] -> 1 is for pre  | 2 is for run | 3 is for post | 4 is for all
        _loopsCounterForSections = list(_executerDict['Forloops'].values())

        # check for trigger
        if _executerDict['Triggers']['enable'] == 'true':
            _triggersActions = [
                _executerDict['Triggers']['run_at_days'],
                _executerDict['Triggers']['run_at_times'],
            ]
        if _executerDict['send_email']:
            if _executerDict['send_email']['enable'] == 'true':
                if _executerDict['send_email']['contact']:
                    triggerEmail = _executerDict['send_email']['contact']
            else:
                triggerEmail = False
        else:
            triggerEmail = False

        return [
            _triggersActions,
            _loopsCounterForSections,
            _preFinal,
            _runFinal,
            _postFinal,
            _executerDict['Abortsectionsifarguemntis'],
            {"Vars": _executerDict['Vars']},
            _argeumntsToFetch,
            triggerEmail
        ]

    # ------- # Methods -> deployAutomatePipeline # ------- #
    def deployAutomatePipeline(
        self,
        sectionPre: list,
        sectionRun: list,
        sectionPost: list,
        forLoopCounterForAllSection: int,
        sectionRunOption: list,
        abortAtArgeument: dict,
        argeumntsToFetch: list,
        varsDict: dict,
        triggerEmail: str
    ):
        """
        - Explain : 
            - Accept list for each section in this order : 
                - sectionPre :
                    - [counter,data]
                - sectionRun
                    - [counter,data]
                - sectionPost
                    - [counter,data]
                - forLoopCounterForAllSection
        - show how to call this function :
            - _pipeLineDataFlow = [
                [_pre,_preLoop],
                [_run,_runLoop],
                [_post,_postLoop],
                _allSectionsLoop
                ] 
            - deployAutomatePipeline(_pipeLineDataFlow[0],_pipeLineDataFlow[1],_pipeLineDataFlow[2],_pipeLineDataFlow[3])
        """
        # init basic vars

        _preData, _preCounter = sectionPre[0], sectionPre[1]
        _runData, _runCounter = sectionRun[0], sectionRun[1]
        _postData, _postCounter = sectionPost[0], sectionPost[1]
        _forLoopCounterForAllSection = int(forLoopCounterForAllSection)
        _startTime = datetime.datetime.now()
        for _loopCounterAllSections in range(0, _forLoopCounterForAllSection):
            log.printLog(
                7, f'{dashLine} # Start Section -> AllSections | for loop counter [{_loopCounterAllSections+1}/{_forLoopCounterForAllSection}] # {dashLine}', 'Section Starting', 1)
            if 'pre' in sectionRunOption:
                for _loopCounterPre in range(0, _preCounter):
                    self.iterateEachSection(
                        'pre',
                        _preData,
                        _loopCounterPre+1,
                        _preCounter,
                        abortAtArgeument,
                        argeumntsToFetch,
                        varsDict
                    )

            if 'run' in sectionRunOption:
                for _loopCounterRun in range(0, _runCounter):
                    self.iterateEachSection(
                        'run',
                        _runData,
                        _loopCounterRun+1,
                        _runCounter,
                        abortAtArgeument,
                        argeumntsToFetch,
                        varsDict
                    )
            if 'post' in sectionRunOption:
                for _loopCounterPost in range(0, _postCounter):
                    self.iterateEachSection(
                        'post',
                        _postData,
                        _loopCounterPost+1,
                        _postCounter,
                        abortAtArgeument,
                        argeumntsToFetch,
                        varsDict
                    )

    # ------- # Methods -> pipeReaderForUsers # ------- #
    def pipeReaderForUsers(self, userToRead: str):
        def triggerUserReadForPipeLine(userToReading: str):
            _userToReading = userToReading.replace('username_', "")
            Utils().spliter()
            _fullPath = os.path.join(
                self.pathFolderUsersCommandExec, f'username_{_userToReading}')
            self.deployMenu(_fullPath)

            log.printLog(
                9, f'Show all the pipelines for user [{_userToReading}] | total pipeline that found [{len(os.listdir(self.pathFolderUserCommandExec))}]')

            Utils().spliter()

        def triggerUserReadForAllPipes():
            _enableWhile = True
            usersPipes = sorted(os.listdir(self.pathFolderUsersCommandExec))
            usersPipes.remove("username_Default")
            usersPipes.append('Quit')
            while _enableWhile:
                for n, i in enumerate(usersPipes, start=1):
                    log.printLog(
                        0, f'Pick [{n}] for  User [{i.replace("username_","")}]')
                _input = input(log.printLog(7, 'Please chose pipe to read : ', statusInBracketTypeStr='input', colorToPickTypeInt=1))
                try:
                    if int(_input) == len(usersPipes):
                        _enableWhile = False
                        log.printLog(0, 'Exit menu.')
                        exit(0)
                    elif int(_input)-1 in [i for i in list(range(0, len(usersPipes)))]:
                        _matchUser = str(usersPipes[int(_input)-1])
                        # _enableWhile = False
                        triggerUserReadForPipeLine(_matchUser)
                    else:
                        log.printLog(
                            2, f'Please make sure you insert number in range (1 - {len(usersPipes)})')
                except ValueError:
                    log.printLog(2, 'Please make sure to insert only number')

        if str(userToRead) == 'Default':
            triggerUserReadForAllPipes()
        else:
            triggerUserReadForPipeLine(userToRead)

    # ------- # Methods -> descriptionReading # ------- #
    def deployMenu(self, pathToPick: str):

        # os.system('sudo python3 -m pip install simple-term-menu')
        os.system('clear')
        from simple_term_menu import TerminalMenu

        _pathForPipes = pathToPick

        main_menu_title = "Pipes menu - Pick user :\n"
        _files = sorted([i for i in os.listdir(_pathForPipes)
                        if '_copy' not in i and '.swp' not in i])

        main_menu_items = [f"{i[0]}. Pipe : {i[1].replace('_.ini','')}" for i in enumerate(
            _files, start=1) if '_copy' not in i]
        main_menu_items.append('Quit')
        main_menu_cursor = ">> "
        main_menu_cursor_style = ("bg_blue", "bold")
        main_menu_style = ("bg_blue", "bold")
        main_menu_exit = False

        main_menu = TerminalMenu(
            menu_entries=main_menu_items,
            title=main_menu_title,
            menu_cursor=main_menu_cursor,
            menu_cursor_style=main_menu_cursor_style,
            menu_highlight_style=main_menu_style,
            cycle_cursor=True,
            clear_screen=False,
        )

        edit_menu_title = "Pipefile user selected\n"
        edit_menu_items = [
            "Copy Execute",
            "Execute Pipe",
            "Edit Pipe",
            "Read Pipe",
            "Delete Pipe",
            # "Run As Debug"
            "Go Back"
        ]
        edit_menu_back = False
        edit_menu = TerminalMenu(
            edit_menu_items,
            title=edit_menu_title,
            menu_cursor=main_menu_cursor,
            menu_cursor_style=main_menu_cursor_style,
            menu_highlight_style=main_menu_style,
            cycle_cursor=True,
            clear_screen=True,
        )
        edit_sel = 0
        while not main_menu_exit:
            main_menu_items = [f"{i[0]}. Pipe : {i[1].replace('_.ini','')}" for i in enumerate(
                _files, start=1) if 'Quit' not in i]
            main_menu_items.append('Quit')
            main_menu = TerminalMenu(
                menu_entries=main_menu_items,
                title=main_menu_title,
                menu_cursor=main_menu_cursor,
                menu_cursor_style=main_menu_cursor_style,
                menu_highlight_style=main_menu_style,
                cycle_cursor=True,
                clear_screen=False,
            )
            main_sel = str(main_menu.show()).replace('\r', '').strip()

            if int(main_sel) < int(len(_files)):

                while not edit_menu_back:
                    edit_sel = str(edit_menu.show()).replace('\r', '').strip()
                    _pathForUser = os.path.join(
                        _pathForPipes, _files[int(main_sel)])
                    # exec Pipe
                    if edit_sel == '0':
                        if os.path.exists(_pathForUser):
                            _readPipe = Reader().readAnyTxtFile(_pathForUser)
                            _pipeName = _pathForUser.split(
                                'pipeline_')[1].split('_.ini')[0]
                            _username = _pathForUser.split(
                                'username_')[1].split('/')[0]
                            _searcher = ['?'+str(i)
                                         for i in list(range(1, 101))]
                            _matchArguemntInPipe = set()
                            _matchArguemntInPipeSentece = set()
                            for i in _readPipe:
                                for n, _eachSearcher in enumerate(_searcher):
                                    if _eachSearcher in str(i).strip():
                                        _matchArguemntInPipeSentece.add(
                                            f'Argeumnt were Found in line [{i}]')
                                        _matchArguemntInPipe.add(_eachSearcher)
                            _matchArguemntInPipe = sorted(_matchArguemntInPipe)
                            if _matchArguemntInPipe:
                                _runner = f'alb -pipe -u {_username} -p {_pipeName} -e -a {" ".join(_matchArguemntInPipe)}'
                            else:
                                _runner = f'alb -pipe -u {_username} -p {_pipeName} -e'

                            log.printLog(
                                1, f'Insert this command to run this pipe : -> \n\t {_runner}')
                            input(log.printColor(3, 'Insert Enter key to exit '))

                    # exec Pipe
                    if edit_sel == '1':
                        if os.path.exists(_pathForUser):
                            _readPipe = Reader().readAnyTxtFile(_pathForUser)
                            _pipeName = _pathForUser.split(
                                'pipeline_')[1].split('_.ini')[0]
                            _username = _pathForUser.split(
                                'username_')[1].split('/')[0]
                            _searcher = ['?'+str(i)
                                         for i in list(range(1, 101))]
                            _matchArguemntInPipe = set()
                            _matchArguemntInPipeSentece = set()
                            for i in _readPipe:
                                for n, _eachSearcher in enumerate(_searcher):
                                    if _eachSearcher in str(i).strip():
                                        _matchArguemntInPipeSentece.add(
                                            f'Argeumnt were Found in line [{i}]')
                                        _matchArguemntInPipe.add(_eachSearcher)
                            _matchArguemntInPipe = sorted(_matchArguemntInPipe)
                            _initWhile = False
                            if _matchArguemntInPipe:
                                _initWhile = True
                                os.system(f'cat {_pathForUser}')
                                Utils().spliter()
                                log.printLog(
                                    0, f'[{len(_matchArguemntInPipe)}] Arguemnt were found.')
                                for _ in _matchArguemntInPipeSentece:
                                    log.printLog(0, _)
                                while _initWhile:
                                    _getArgFromUser = input(log.printColor(
                                        3, f'Total of [{len(_matchArguemntInPipe)}] found , Please add them here , each space repsent as new arguemnt : '))
                                    if len(_getArgFromUser.split(' ')) == len(_matchArguemntInPipe):
                                        _initWhile = False
                                        log.printLog(
                                            1, 'Match argument as needed , approve to deploy pipe.')

                                        os.system(
                                            f'{Reader().extractorFilePathFromAlbertConfigFiles("lib/pipeline.py")} -u {_username} -p {_pipeName} -e -a {_getArgFromUser.strip()}')
                                        exit(0)

                                    else:
                                        log.printLog(
                                            2, f'You are missing arguemnt in your input - current Arg [{len(_getArgFromUser.split(" "))}/{len(_matchArguemntInPipe)}], Please try again.')
                            else:
                                os.system(f'cat {_pathForUser}')
                                Utils().spliter()
                                log.printLog(
                                    0, f'No arguemnt found trigger the pipe from here.')
                                os.system(
                                    f'{Reader().extractorFilePathFromAlbertConfigFiles("lib/pipeline.py")} -u {_username} -p {_pipeName} -e')

                                exit(0)
                            time.sleep(2)
                        else:
                            log.printLog(
                                2, f'Its seems like the pipe is delete or missing in the file system , Please check the location : [{_pathForUser}]')
                            time.sleep(2)
                    # Edit Pipe
                    if edit_sel == '2':
                        if os.path.exists(_pathForUser):
                            os.system(f'sudo vim {_pathForUser}')
                        else:
                            log.printLog(
                                2, f'Its seems like the pipe is delete or missing in the file system , Please check the location : [{_pathForUser}]')
                            time.sleep(2)
                    # Read Pipe
                    elif edit_sel == '3':
                        if os.path.exists(_pathForUser):
                            os.system(f'cat {_pathForUser}')
                            input(log.printColor(3, 'Insert Enter key to exit '))
                        else:
                            log.printLog(
                                2, f'Its seems like the pipe is delete or missing in the file system , Please check the location : [{_pathForUser}]')
                            time.sleep(2)
                    # Delete Pipe
                    elif edit_sel == '4':
                        if os.path.exists(_pathForUser):

                            os.system(f'cat {_pathForUser}')
                            _getApprove = input(log.printColor(
                                3, f'[Warning] You about to delete pipe [{_pathForUser}] , Please approve by insert [1=Okay/anyOtherKey=no] : '))
                            if _getApprove == '1':
                                log.printLog(
                                    7, f'Delete pipe [{_pathForUser}]', 'Delete Pipe', 3)
                                os.system(
                                    f'sudo cp -r {_pathForUser} {_pathForUser.replace(".ini",Utils().getAutoTime(returnDataAndTimeNoMilsec=True))}_copy.ini')
                                os.system(f'sudo rm -r {_pathForUser}')
                                edit_menu_back = True
                                time.sleep(5)
                            else:
                                log.printLog(
                                    7, f'Ignore delete pipe [{_pathForUser}]', 'Ignore Delete Pipe', 3)
                                time.sleep(2)
                        else:
                            log.printLog(
                                2, f'Its seems like the pipe is delete or missing in the file system , Please check the location : [{_pathForUser}]')
                            time.sleep(2)
                    # go back
                    # elif edit_sel == '5':
                    elif edit_sel == '5':
                        edit_menu_back = True
                        print("Back Selected from pipeline : ",
                              _files[int(main_sel)])
                edit_menu_back = False
            elif main_sel == str(len(_files)):
                main_menu_exit = True
                edit_menu_back = True
                print("Quit Selected")
                # exit(0)
            with open('t.txt', 'w') as wr:
                wr.write(
                    f'{str(edit_sel)} {str(main_sel)} {str(len(_files))}'+'\n')

    # ------- # Methods -> descriptionReading # ------- #
    def descriptionReading(self, userName: str, pipeName: str):
        _loadedPipelind = self.readPipelineFile()
        log.printLog(
            0, f'Loaded Description for user [{userName}] | pipeline [{pipeName}]')
        Utils().spliter()
        print(_loadedPipelind['Pipelineinfo']['description'])
        Utils().spliter()
        print(log.printColor(5, f'# !! # Auto suggest to run # !! #'))
        print(log.printColor(5, f'alb -pipe -u {userName} -p {pipeName} -r'))

    # ------- # Methods -> execPipeline # ------- #
    def execPipeline(self, sectionRunOption: list, argeumntsToFetch: list = False):
        _startTime = datetime.datetime.now()
        Utils().spliter()
        log.printLog(
            7, f'wellcome user [{self.nameUser.capitalize()}] , running pipeline [{self.pipeName}].', 'WellcomeMessage', 5)
        Utils().spliter()
        _triggersActions, _loopsCounterForSections, _pre, _run, _post, _abortAtArgeument, varsDict, _argeumntsToFetch, triggerEmail = self.parserAllSections(
            argeumntsToFetch=argeumntsToFetch)
        # loops
        _preLoop = int(_loopsCounterForSections[0])
        _runLoop = int(_loopsCounterForSections[1])
        _postLoop = int(_loopsCounterForSections[2])
        _allSectionsLoop = int(_loopsCounterForSections[3])
        # create pipeline data format
        _pipeLineDataFlow = [
            [_pre, _preLoop],
            [_run, _runLoop],
            [_post, _postLoop],
            _allSectionsLoop
        ]

        # trigger
        _makeWhile = False
        _runAtDays = False
        _runAtTimes = False
        _openInNewTerminal = False

        if _triggersActions:
            _makeWhile = True
            _runAtDays = [int(i) for i in _triggersActions[0].split(' ')]
            _runAtTimes = _triggersActions[1].split(' ')[0]

        if _makeWhile:
            log.printLog(
                7, f'Deploy trigger to run at days [{_runAtDays}] , at time [{_runAtTimes}] , new terminal open [{_openInNewTerminal}]', 'Activated trigger action', 4)
            _commandToRun = "alb -pipe "+" ".join(sys.argv[1::])
            _commandToRun = [_commandToRun.replace(' ', '..').strip().replace(
                '\n', '').replace('\t', '').replace('\r', '')]
            self.deployAutomatePipeline(
                _pipeLineDataFlow[0],
                _pipeLineDataFlow[1],
                _pipeLineDataFlow[2],
                _pipeLineDataFlow[3],
                sectionRunOption=sectionRunOption,
                abortAtArgeument=_abortAtArgeument,
                argeumntsToFetch=_argeumntsToFetch,
                varsDict=varsDict,
                triggerEmail=triggerEmail
            )
            exit(0)
        else:
            self.deployAutomatePipeline(
                _pipeLineDataFlow[0],
                _pipeLineDataFlow[1],
                _pipeLineDataFlow[2],
                _pipeLineDataFlow[3],
                sectionRunOption=sectionRunOption,
                abortAtArgeument=_abortAtArgeument,
                argeumntsToFetch=_argeumntsToFetch,
                varsDict=varsDict,
                triggerEmail=triggerEmail

            )
        _totalTime = datetime.datetime.now()-_startTime
        exit(0)


if __name__ == "__main__":
    Utils().spliter()
    log.printLog(0, f'Pipeline auto generated Id -> [{scriptRandomNumber}]')
    Utils().spliter()

    args = configParser().parse_args()
    _checkArgs = [args.pipe_name, args.user, args.section_run]
    if all(_checkArgs):
        _pipelineInstations = Pipeline(
            pipelineName=_checkArgs[0], username=_checkArgs[1])
        # ------- # Arguments -> -read -> example 1 # ------- #
        if args.read:
            _pipelineInstations.readPipelineFile()
            os.system(f'cat {_pipelineInstations.pathFileCommandUser}')
            exit(0)
        # ------- # Arguments -> -write -> example 2 # ------- #
        elif args.write:
            _pipelineInstations.readPipelineFile()
            os.system(f'sudo vim {_pipelineInstations.pathFileCommandUser}')
            exit(0)
        # ------- # Arguments -> -exec -> example 2 # ------- #
        elif args.deploy_auto_tamplate:
            _pipelineInstations.createAutoPipelineAutomation(args.user)
            exit(0)
        # ------- # Arguments -> -exec -> example 2 # ------- #
        elif args.exec:

            _pathFolderLoggingData = os.path.join(Reader().extractorFilePathFromAlbertConfigFiles(
                "log"), 'pipeline_logging_data', f'pipeUser_{_checkArgs[1]}', f'pipeName_{_checkArgs[0]}', f'PipeId_{scriptRandomNumber}')
            _pathFileLoggingData = os.path.join(
                _pathFolderLoggingData, 'pipeline_logging.txt')
            log.printLog(
                0, f'Logging data is going to save on this folder [{_pathFileLoggingData}]')

            _pipelineInstations.readPipelineFile()
            _pipelineInstations.execPipeline(args.section_run, args.arguments)
            exit(0)
        # ------- # Arguments -> -exec -> example 2 # ------- #
        elif args.description:
            _pipelineInstations.descriptionReading(
                userName=_checkArgs[1],
                pipeName=_checkArgs[0])

            exit(0)
    elif args.show:
        Pipeline(pipelineName='default',
                 username=_checkArgs[1]).pipeReaderForUsers(_checkArgs[1])
    elif args.example:
        _command = " ".join(Utils().searchAlbertInisdeWords('alb -pipe -u admin -p sample -e'))
        log.printLog(0,'Showing example ...')
        log.printLog(0,f'Deploy the command -> {_command} in 3 sec')
        time.sleep(3)
        Utils().spliter()
        os.system(_command)
        Utils().spliter()
    else:
        print('error')
        exit(0)

