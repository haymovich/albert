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
import paramiko
import socket
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
        - The abaility to send command to linux host / windows host
    """
    def __init__(
        self,
        passwordTypeStr:str,
        portNumberTypeStr:str,
        ):
        # ------- # Default attributes -> basic Variable # ------- #
        self.passwordTypeStr = passwordTypeStr
        self.portNumber = portNumberTypeStr
        self.machineTypesTypeStr = ['linux','windows']
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #
    # ------- # Methods -> sendCommand # ------- #
    def sendCommand(
        self,
        showLoggerPrintTypeBool:bool=True,
        returnLogTypeBool:bool=False,
        totalTimputTypeInt:int=120,
        getOutputFromSystemTypeBool:bool=True,
        **args,
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
        - Needed Args : 
            hostIpTypeStr:str,
            commandToSendTypeStr:str,
            machineTypeWindowsOrLinuxTypeStr:str,

        """
        # init basic var
        timeout = totalTimputTypeInt
        args["port"] = self.portNumber
        args["username"] = "wiliotlab"
        args["password"] = self.passwordTypeStr
        args['timeout-converted'] = f'{int(int(timeout)*0.0166666667)}'
        try:
            # check machine type
            if args["machineTypeWindowsOrLinuxTypeStr"] not in self.machineTypesTypeStr:
                log.printLog(2,f"Machine type must be one of both -> [{self.machineTypesTypeStr}]")
                exit(0)
            else:
                # machine type --> linux
                if args["machineTypeWindowsOrLinuxTypeStr"] == self.machineTypesTypeStr[0]:
                    pass
                # machine type --> windows
                if args["machineTypeWindowsOrLinuxTypeStr"] == self.machineTypesTypeStr[1]:
                    pass
            # print
            if showLoggerPrintTypeBool:
                Utils().showDataWhenParsing(args,40)

            # Make the connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(args["hostIpTypeStr"], args["port"], args["username"], args["password"])
            # send the command
            stdin, stdout, stderr = ssh.exec_command(args["commandToSendTypeStr"],timeout=timeout)
            catchLogPrint = ['Fetching Data ......']
            # try:
            catchLogPrint = stdout.readlines()
            # return the print
            if args["commandToSendTypeStr"]:
                log.printLog(0,'Please wait for output log.')
                for output in catchLogPrint:
                    output = str(output).replace("\n","")
                    log.printNoFormat(f' - {output}')
                log.printLog(0,f'Commnad was send to machine type [{args["machineTypeWindowsOrLinuxTypeStr"]}] via host [{args["hostIpTypeStr"]}].')
            # return what data is in the log
            if returnLogTypeBool:
                return [i.replace('\n', '') for i in catchLogPrint]
            if getOutputFromSystemTypeBool:
                log.printNoFormat(Utils().dashLine)
        except (paramiko.ssh_exception.SSHException,socket.timeout):
            pass
        except TimeoutError:
            pass

if __name__ == "__main__":

    args = configParser().parse_args()
    # ------- # Arguments -> -e1 -> example 1 # ------- #
    if args.testing:
        RemoteCommand("Qwert-2023$",'22').sendCommand(hostIpTypeStr='192.168.48.49',commandToSendTypeStr='ls -al',machineTypeWindowsOrLinuxTypeStr='linux')
    # ------- # Arguments -> -e2 -> example 2 # ------- #
    elif args.example_2:
        pass


