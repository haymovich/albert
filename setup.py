#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<SCRIPT EXAPLAIN>
"""
import os
import sys
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(pathScriptFolder, 'lib'))
from utils import Utils
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-setup' 


if __name__ == "__main__":

    Utils().installLib()
    Utils().checkLib()
