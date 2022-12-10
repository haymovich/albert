#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch
@Auther Email - bar.rose65@gmail.com

<SCRIPT EXAPLAIN>
"""
import argparse
import subprocess
import os
import datetime
from logger import logger
import sys
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-st' # scriptTemplate will be -st
# ------- # Outside Variable - visual && usefull variable # ------- #
# scriptRandomNumber = Switz().randomNumber()
# getCurrnetHostname = Switz().getHostname()
# class ArgumentParserError(Exception): pass
# class ThrowingArgumentParser(argparse.ArgumentParser):
#     def error(self, message):
#         raise ArgumentParserError(message)
startTime = datetime.datetime.now()
dashLine = '-------------------------------------------'
currentSite = 'site_0'

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
# ------- # Class -> tamplateClass # ------- #
class tamplateClass():
    """
    - Exaplain :
        - Example this tamplate class
    """
    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #

    # ------- # Methods -> method # ------- #
    def deploy(self):
        pass

if __name__ == "__main__":

    args = configParser().parse_args()
    # ------- # Arguments -> -e1 -> example 1 # ------- #
    if args.example_1:
        pass
    # ------- # Arguments -> -e2 -> example 2 # ------- #
    elif args.example_2:
        pass

