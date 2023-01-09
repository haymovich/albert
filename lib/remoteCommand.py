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
import sys
from utils import Utils
Utils().checkLib()

# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-remote_command'
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
log = logger(enableSave=False)
# ------- # Try - Import paramiko # ------- #
# Switz().checkLib()
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
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

# ------- # Class -> RemoteCommand # ------- #
class RemoteCommand():
    """
    - Exaplain :
        - Example this tamplate class
    """
    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #
    # ------- # Methods -> sendCommandToNuc # ------- #
    def send(
        self,
        hostIpTypeStr:str,
        commandToSendTypeStr:str,
        machineTypeWindowsOrLinuxTypeStr:str,
        getOutputFromSystemTypeBool:bool,
        showLoggerPrintTypeBool:bool=True,
        returnLogTypeBool:bool=False,
        totalTimputTypeInt:int=120
        ):
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
        # init basic var
        
        try:
            machineType = machineTypeWindowsOrLinuxTypeStr
            machineUsernameIdentify = ''
            host = f'{hostIpTypeStr}'

            # check machine type
            if machineType not in self.machineTypesTypeStr:
                log.printLog(2,f"Machine type must be one of both -> [{self.machineTypesTypeStr}]")
                exit(0)
            else:
                # machine type --> linux
                if machineType == self.machineTypesTypeStr[0]:
                    #  haifa
                    # print(hostIpTypeStr)
                    if '143.185.' in str(hostIpTypeStr) or 'ladh' in str(hostIpTypeStr):
                        machineUsernameIdentify = self.checkSuperUser( str(hostIpTypeStr),self.readJsonDataFromMappingFile['site_0']['systemPath']['superUser'])
                        # machineUsernameIdentify = self.readJsonDataFromMappingFile['site_0']['systemPath']['superUser']
                    # jer
                    else:
                        machineUsernameIdentify = self.checkSuperUser( str(hostIpTypeStr),self.readJsonDataFromMappingFile['site_1']['systemPath']['superUser'])
                        # machineUsernameIdentify = self.readJsonDataFromMappingFile['site_1']['systemPath']['superUser']
                        # print(machineUsernameIdentify)
                # machine type --> windows
                if machineType == self.machineTypesTypeStr[1]:
                    machineUsernameIdentify = self.readJsonDataFromMappingFile["site_1"]["authentication"]["username"]
            timeout = totalTimputTypeInt   
            port = self.portNumber
            username = machineUsernameIdentify
            password = self.passwordTypeStr
            # print
            if showLoggerPrintTypeBool:
                pass
                log.printLog(0,f'Set hostname to [{host}]')
                log.printLog(0,f'Set machine type to [{machineType}]')
                log.printLog(0,f'Set username to [{username}]')
                # log.printLog(0,f'Set port number to [{port}]')
                log.printLog(0,f'Set ssh timeout to [{int(int(timeout)*0.0166666667)} min]')
                log.printLog(0,f'Set command value to [{commandToSendTypeStr}]')
            # Make the connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            # send the command
            stdin, stdout, stderr = ssh.exec_command(commandToSendTypeStr,timeout=timeout)
            catchLogPrint = ['Fetching Data ......']
            # try:
            catchLogPrint = stdout.readlines()
            # except:

            #     catchLogPrint =  stdout.readlines()
            #     for line in catchLogPrint:
            #         print(line.decode("utf8", "ignore"))

            # return the print
            if getOutputFromSystemTypeBool:
                log.printLog(0,'Please wait for output log.')
                for output in catchLogPrint:
                    output = str(output).replace("\n","")
                    log.printNoFormat(f' - {output}')
                log.printLog(0,f'Commnad was send to machine type [{machineType}] via host [{host}].')
            # return what data is in the log
            if returnLogTypeBool:
                return [i.replace('\n', '') for i in catchLogPrint]
            if getOutputFromSystemTypeBool:
                log.printNoFormat(dashLine)
        except (paramiko.ssh_exception.SSHException,socket.timeout):
            pass
        except TimeoutError:
            pass

if __name__ == "__main__":

    args = configParser().parse_args()
    # ------- # Arguments -> -e1 -> example 1 # ------- #
    if args.example_1:
        pass
    # ------- # Arguments -> -e2 -> example 2 # ------- #
    elif args.example_2:
        pass


