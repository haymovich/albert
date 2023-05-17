#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<SCRIPT EXAPLAIN>
"""
import argparse
import subprocess
import os
import datetime
from logger import logger
from reader import Reader
from writer import Writer
import sys
import threading
import time
import re
import subprocess
from utils import Utils
# ------- # Try - Import paramiko # ------- #
Utils().checkLib()
import paramiko
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-netscan' 
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
log = logger(enableSave=False)
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)


# ------- # Outside function -  # ------- #
def killThread(osGetPid):
    _currentSystemPid = osGetPid
    _commandToExec  = f'sudo kill -9 {_currentSystemPid}'
    log.printLog(0,f'Kill thread pid -> [{_currentSystemPid}] with command -> [{_commandToExec}]')
    os.system(_commandToExec)
# ------- # Outside function - configParser # ------- #
def configParser():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-e1", "--example_1", help="this is example args number 1", type=str, required=False, default=None)
    parser.add_argument("-e2", "--example_2", help="this is example args number 1 - True or False", required=False, action='store_true', default=False)
    parser.add_argument("-t", "--testing", help="run all command inside testing variable", required=False, action='store_true', default=False)
    parser.add_argument("-save_log", "--save_log", help="Save Logger to extranal file , give path like --> /home/sv10g/", required=False, default=False)
    
    return parser
# ------- # Class -> tamplateClass # ------- #
class NetworkScanner():
    """
    - Exaplain :
        - Example this tamplate class
    """
    def __init__(self,
        password:str,
        username:str,
        portNumber:str,
        ):
        # ------- # Default attributes -> basic Variable # ------- #
        self.password = password
        self.username = username
        self.portNumber = portNumber
        self.basicJsonDumperForStoreHosts = {
            'hostsScanned':{},
            'hostCredsUsername':{},
            'hostCredsPass':{},
            'timestempHosts':{},
            'timestempFromPrivateDnsPoolScript':'',
            'totalMappedIpsHosts':'',
            'totalMappedTimestempHosts':''

        }
        self.credsBasicDumper = {
            'username1':'password1',
            'username2':'password2'
        }
        self.hostsnameWithIpTypeDict ={}
        # ------- # Default attributes -> Names # ------- #
        self.nameStoreHostsJsonFileName = 'networkScanHosts.json'
        self.nameCredsJsonName = 'creds.json'
        # ------- # Default attributes -> Path # ------- #
        self.pathStoreHosts = os.path.join(Reader().extractorFilePathFromAlbertConfigFiles('config'),self.nameStoreHostsJsonFileName)
        self.pathCredsJson = os.path.join(Reader().extractorFilePathFromAlbertConfigFiles('config'),self.nameCredsJsonName)
        if not os.path.exists(self.pathStoreHosts):
            Writer().writeAnyJsonFile(
                jsonFileLocationTypeStr=self.pathStoreHosts,
                dataToWriteTypeDict=self.basicJsonDumperForStoreHosts
            )
        elif not os.path.exists(self.pathCredsJson):
            Writer().writeAnyJsonFile(
                jsonFileLocationTypeStr=self.pathCredsJson,
                dataToWriteTypeDict=self.credsBasicDumper
            )
    # ------- # Methods -> getUserInput # ------- #
    def getIpFormatFromUser(
        self,
        autoUserInputTypeStr:str=False,
        ):
        # init basic variable
        _whileVariable = True
        _getUserInputForIp = ''

        while _whileVariable:
            try:
                # user input
                if not autoUserInputTypeStr:
                    # sentce
                    _senteceWithColor = 'Please insert your ip first 3 octact , for example [1.1.1/2.2.2/3.3.3] : '
                    _getUserInputForIp = input(_senteceWithColor)
                # machine auto input
                elif autoUserInputTypeStr:
                    _getUserInputForIp = autoUserInputTypeStr
                # search ip inside user input
                _searchThe3OctatInStr = re.findall(re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}'),_getUserInputForIp)
                # search has been found
                if _searchThe3OctatInStr:
                    # print
                    log.printLog(
                        0,
                        f'Found matchine ip segemnt [{_searchThe3OctatInStr[0]}] continue to mapping this network')
                    _whileVariable = False
                    return _searchThe3OctatInStr[0] 
                else:
                    log.printLog(2,'You must insert 3 octact to continue to mapping network.')
            except ValueError:
                log.printLog(2,'You insert an alphabent latter , please try again.')
    # ------- # Methods -> sendCommandToNuc # ------- #
    def extractHostnameViaSSHCommand(self,hostIpTypeStr:str):
        """
        - Explain : 
            - Send Command to nuc , Seprated function due to diffrent autherntination value from nuc to host
        
        - Flags :
            - commandToSendTypeStr : 
                - What command wil be send to the nuc ?
            - getOutputFromSystemTypeBool :
                - True  -> get the output from the command exec
                - False -> pass
        """
        try:
            ssh = None
            host = f'{hostIpTypeStr}'
            port = self.portNumber
            username = self.username
            password = self.password
            # Make the connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            # send the command
            stdin, stdout, stderr= ssh.exec_command('hostname')
            extractHostName = stdout.readlines()
            # if hostname exists
            if extractHostName:
                extractHostName = str(extractHostName[0]).replace('\n','').replace('\r','').strip()
                log.printLog(1,f'Found new hostname [{extractHostName}] to ip [{hostIpTypeStr}]')
                self.hostsnameWithIpTypeDict[extractHostName] = hostIpTypeStr
        except:
            pass
    # ------- # Methods -> deployAutoMapperForDns # ------- #
    def extractLiveHostViaPingAndHostNameRemotly(
        self,
        mapNetworkFromUserInputTypeList:list,
        timeoutForCommunicatePingTypeFloat=0.05,
        ):
    
        # mapp all the ip inside this network
        for _num, _singleHostIp in enumerate(mapNetworkFromUserInputTypeList,start=1):
            _sentece = f"Please Wait - Total {_num} Out Of 254 ip Has Mapped.\r".strip()
            sys.stdout.write(f"[Info] Please Wait - Total {_num} Out Of 254 ip Has Mapped.\r")
            # sys.stdout.write(_sentece)
            sys.stdout.flush()
            try:
                _sendPingToHost = subprocess.Popen(['ping', '-c1', _singleHostIp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _sendPingToHost.communicate(timeout=timeoutForCommunicatePingTypeFloat)
            except subprocess.TimeoutExpired:
                    pass
            else:
                # start Thread
                try:
                    _startThread = threading.Thread(target=self.extractHostnameViaSSHCommand,args=(str(_singleHostIp),),daemon=True)
                    _startThread.start()
                    _startThread.terminate()
                    _startThread.join()
                except:
                    pass  
    # ------- # Methods -> compereExistsHostToOldHost # ------- #
    def compereExistsHostIpToOldHostIp(self):
        # init variables
        _readPrivateDnsHosts = Reader().readHostScannedPool()['hostsScanned']
        _listForAllIpHostsInValues = list(_readPrivateDnsHosts.values())

        _setForIps = set()
        _setForHosts = set()
        for _hostaName,_hostIp in _readPrivateDnsHosts.items():
            if _listForAllIpHostsInValues.count(_hostIp) > 1:
                _setForHosts.add(_hostaName)
                _setForIps.add(_hostIp)
        
        if len(_setForHosts) == 0 or len(_setForIps) == 0:
            log.printLog(1,'No dupplicated hosts were founded.')
        else:
            log.printLog(7,'Dupplicated hosts were founded.','Warning',3)
    # ------- # Methods -> compereExistsHostToOldHost # ------- #
    def writeHostsToPrivateDnsJsonFile(self):
        # init variables
        _readPrivateDnsHosts = Reader().readHostScannedPool()
        # print
        log.printLog(0,f'Start compering total [{len(self.hostsnameWithIpTypeDict)}] hosts.')
        # writing data to private var
        for _hostName,_hostIp, in self.hostsnameWithIpTypeDict.items():
            _readPrivateDnsHosts['hostsScanned'][_hostName] = _hostIp
            _readPrivateDnsHosts['hostCredsUsername'][_hostName] = self.username
            _readPrivateDnsHosts['hostCredsPass'][_hostName] = self.password
            
            _readPrivateDnsHosts['timestempHosts'][_hostName] = str(datetime.datetime.now())
            _readPrivateDnsHosts['timestempFromPrivateDnsPoolScript'] = str(datetime.datetime.now())
        # append the len of total hosts 
        _readPrivateDnsHosts['totalMappedIpsHosts'] = str(len(_readPrivateDnsHosts['hostsScanned']))
        _readPrivateDnsHosts['totalMappedTimestempHosts'] = str(len(_readPrivateDnsHosts['timestempHosts']))
        # write the results to map json file 
        Writer().writeAnyJsonFile(self.pathStoreHosts,_readPrivateDnsHosts)
        # WriteJson().writeToPrivateDnsJsonFile(_readPrivateDnsHosts)
        # clear the current hostnames
        self.hostsnameWithIpTypeDict.clear()  
    # ------- # Methods -> deployAutoMapperForDns # ------- #
    def deployAutoMapperForDns(
        self,
        autoUserInputTypeStr:str=False,
        userInputMethodTypeBool:bool=False,
        automationMethodTypeBool:bool=False,
        timeoutForCommunicatePingTypeFloat=0.05,

        ):
        # init basic var
        _timeoutForCommunicatePingTypeFloat = timeoutForCommunicatePingTypeFloat
        _activatedMethodBy = 'Automation'
        _getIpFormatFromUser = ''
        _autoUserInputTypeStr = autoUserInputTypeStr
        _mappedNewNetworkFromUserFormatIp = ''

        # automated from the user
        if userInputMethodTypeBool:
            _activatedMethodBy = 'User'
            _autoUserInputTypeStr = False
            _getIpFormatFromUser = self.getIpFormatFromUser(autoUserInputTypeStr=_autoUserInputTypeStr)
        # automated from the machine
        if automationMethodTypeBool:
            _activatedMethodBy = 'Automation'
            _getIpFormatFromUser = self.getIpFormatFromUser(autoUserInputTypeStr=_autoUserInputTypeStr)
        # format the netwrok
        _mappedNewNetworkFromUserFormatIp = ['{}.{}'.format(_getIpFormatFromUser, i) for i in range(1, 255)]
        _blackList = ['192.168.48.1']
        """
        192.168.1.1
        """
        try:
            for i in _blackList:
                log.printLog(7,f'remove black list ip [{i}]','remove-blacklist-ip',3)
                _mappedNewNetworkFromUserFormatIp.remove(i)
        except:
            pass
        if [i for i in _mappedNewNetworkFromUserFormatIp if i in _blackList]:
            log.printLog(2,f'cannot continue with the script due to {_blackList} in the list.')
        # print info
        log.printLog(7,f'Set Arguemnts Value [timeoutForCommunicatePingTypeFloat] To [{_timeoutForCommunicatePingTypeFloat}]','MethodInfo',3)
        log.printLog(7,f'Set Arguemnts Value [automationMethodTypeBool]           To [{_activatedMethodBy}]','MethodInfo',3)
        log.printLog(7,f'Set Arguemnts Value [userInputMethodTypeBool]            To [{userInputMethodTypeBool}]','MethodInfo',3)
        log.printLog(7,f'Set Arguemnts Value [getIpFormatFromUser]                To [{_getIpFormatFromUser}]','MethodInfo',3)
        log.printLog(7,f'Set Arguemnts Value [autoUserInputTypeStr]               To [{_autoUserInputTypeStr}]','MethodInfo',3)


        # start the mapping logic
        self.extractLiveHostViaPingAndHostNameRemotly(
            mapNetworkFromUserInputTypeList=_mappedNewNetworkFromUserFormatIp,
            timeoutForCommunicatePingTypeFloat=_timeoutForCommunicatePingTypeFloat)

        # compering old to new hosts
        self.writeHostsToPrivateDnsJsonFile()
        self.compereExistsHostIpToOldHostIp()
    

if __name__ == "__main__":

    # ------- # Methods -> deployAutomaticScan # ------- #

    args = configParser().parse_args()
    # ------- # Arguments -> -e1 -> example 1 # ------- #
    if args.example_1:
        pass
    # ------- # Arguments -> -e2 -> example 2 # ------- #
    elif args.example_2:
        pass
    # ------- # Arguments -> -e2 -> example 2 # ------- #
    elif args.testing:
        initer = NetworkScanner('','','')
        def deployAutomaticScan(credsForScanning:dict=False,netForScanning:list=False):
            # init basic vars
            _creds = Reader().readAnyJsonFile(os.path.join(Reader().extractorFilePathFromAlbertConfigFiles('config'),'creds.json'))
            if _creds == initer.credsBasicDumper:
                log.printLog(2,'Please make sure you change the default creds file before using automation.')
                exit(0)
            _netForScanning = ['192.168.48']
            _credsForScanning = _creds if not credsForScanning else credsForScanning
            _netForScanning = _netForScanning if not netForScanning else netForScanning
            for _username,_pass in _credsForScanning.items():
                _builder = NetworkScanner(password=_pass,username=_username,portNumber='22')
                for _eachMapItem in _netForScanning:
                    # start time title
                    _builder.deployAutoMapperForDns(
                        autoUserInputTypeStr=_eachMapItem,
                        automationMethodTypeBool=True,
                        userInputMethodTypeBool=False,
                        timeoutForCommunicatePingTypeFloat=0.05,
                        )
        deployAutomaticScan()


