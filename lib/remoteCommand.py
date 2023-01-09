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
# ------- # Try - Import paramiko # ------- #
Utils().checkLib()
import paramiko
import socket
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-remote_command'
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
log = logger(enableSave=True)
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
        - The abaility to send command to linux host / windows host
    """
    def __init__(
        self,
        password:str,
        username:str,
        portNumber:str,
        ):
        # ------- # Default attributes -> basic Variable # ------- #
        self.password = password
        self.username = username
        self.portNumber = portNumber
        self.machineTypes = ['linux','windows']
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #
    # ------- # Methods -> sendCommand # ------- #
    def sendCommand(
        self,
        hostIp:str,
        commandToSend:str,
        machineType:str,
        getOutputFromSystem:bool=True,
        showLoggerPrint:bool=True,
        returnLog:bool=False,
        totalTimeoutInSec:int=120
        ):
        """
        - Explain : 
            - Send Command to nuc , Seprated function due to diffrent autherntination value from nuc to host
        
        - Flags :
            - commandToSend : 
                - What command wil be send to the nuc ?
            - getOutputFromSystem :
                - True  -> get the output from the command exec
                - False -> pass
        """
        # init basic var
        timeout = totalTimeoutInSec   
        port = self.portNumber
        username = self.username
        password = self.password
        _res = ['...deployCommand']
        try:
            machineType = machineType
            host = f'{hostIp}'
            # check machine type
            if machineType not in self.machineTypes:
                log.printLog(2,f"Machine type must be one of both -> [{self.machineTypes}]")
                exit(0)
            else:
                # machine type --> linux
                if machineType == self.machineTypes[0]:
                    pass
                # machine type --> windows
                if machineType == self.machineTypes[1]:
                    pass
            # print
            if showLoggerPrint:
                _locals = locals()
                # pop
                [ _locals.pop(i) for i in ['self','host','totalTimeoutInSec']]
                # convert
                _locals['timeout'] = f'{int(int(timeout)*0.0166666667)} min'
                _locals['password'] = '*'*len(password)

                Utils().showDataWhenParsing(_locals,45)
            # Make the connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            # send the command
            stdin, stdout, stderr = ssh.exec_command(commandToSend,timeout=timeout)
            catchLogPrint = ['Fetching Data ......']
            # try:
            catchLogPrint = stdout.readlines()
            # return the print
            if getOutputFromSystem:
                log.printLog(0,'Please wait for output log.')
                for output in catchLogPrint:
                    output = str(output).replace("\n","")
                    log.printNoFormat(f' - {output}')
                log.printLog(0,f'Commnad was send to machine type [{machineType}] via host [{host}].')
            # return what data is in the log
            if getOutputFromSystem:
                log.printNoFormat(Utils().dashLine)

            _res =  [i.replace('\n', '') for i in catchLogPrint]
        except (paramiko.ssh_exception.SSHException,socket.timeout):
            pass
        except TimeoutError:
            pass

        return _res
if __name__ == "__main__":

    args = configParser().parse_args()
    # ------- # Arguments -> -e2 -> example 2 # ------- #
    if args.example_2:
        pass
    # ------- # Arguments -> -e1 -> example 1 # ------- #
    elif args.testing:
        print(RemoteCommand('PASS','USERNAME','PORTNUMBER').sendCommand("IPADD",'HOSTNAME','LINUX'))



