#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch

<SCRIPT EXAPLAIN>
"""
import argparse
import os
import datetime
import sys
import __main__
import logging
from reader import Reader

# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-lg'
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
dashLine = '-------------------------------------------'
logCounter = 0
outputFileContantTypeList = []
changeOnlyOnce = True
outputFile = ''
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
scriptName = sys.argv[0].replace(
    './', '').strip().replace('.py', '')
outsideScriptName = str(__main__.__file__).split(
    '/')[::-1][0].strip().split('.')[0].strip().replace('_', '').strip()
nameFileForLogFile = datetime.datetime.now().strftime(
    f"{Reader().extractorFilePathFromAlbertConfigFiles('log')}FileName_{outsideScriptName}_Date_%d-%m-%Y_Time_%H-%M-%S-%f.log")

# ------- # Class -> logger # ------- #
class logger:
    """
    - Explain :
        - print with color inside user interface
    - Available methods :
        - info : blueColor | Bold
            - info for something like ip address / hostname
        - pass : greenColor | Bold
            - test pass
        - failed : failColor | Bold
            - test failed
        - check started : yellowColor | Bold
            - start to checking something
        - check ended : yellowColor | Bold
            - end to checking something
        - change : turquoiseColor | Bold
            - something that change like ip address
        - costumeInfo : color white
            - able to print what the user want
    - Comment :
        - Add Style && info about what happened in system.
    """

    def __init__(
        self,
        enableSave: bool = False
    ):
        # ------- # Default attributes -> color Variable # ------- #
        self.colorMap = {
            0: "",  # white
            1: '\033[94m',  # blue
            2: '\033[91m',  # red
            3: '\033[93m',  # yellow
            4: '\033[96m',  # turquoise
            5: '\033[92m',  # green
            6: '\033[95m',  # green
        }
        # ------- # Default attributes -> basic Variable # ------- #
        self.optionsLogger = {
            0: {'status': f'[Info]', 'color': self.colorMap[1]},
            1: {'status': f'[Pass]', 'color': self.colorMap[5]},
            2: {'status': f'[Failed]', 'color': self.colorMap[2]},
            3: {'status': f'[Check Started]', 'color': self.colorMap[3]},
            4: {'status': f'[Check Ended]', 'color': self.colorMap[3]},
            5: {'status': f'[Change]', 'color': self.colorMap[4]},
            6: {'status': f'[Ignoring]', 'color': self.colorMap[4]},
            # 7:{'status':f' [{outsideScriptName} - {statusInBracketTypeStr}]','color':self.colorMap[0]},
            8: {'status': f'[Init]', 'color': self.colorMap[4]},
            9: {'status': f'[Activated]', 'color': self.colorMap[0]},
            10: {'status': f'[Checking]', 'color': self.colorMap[4]},
            11: {'status': f'[Warning]', 'color': self.colorMap[4]},

        }
        # ------- # Default attributes -> option To Colors # ------- #
        self.endOfLine = '\033[0m'
        self.makeBold = '\033[1m'
        self.makeUnderline = '\033[4m'
        # ------- # Default attributes -> Names # ------- #

        # ------- # Default attributes -> Logger Variable # ------- #
        self.loggerWrapperFormat = '%(asctime)s %(levelname)-3s | %(message)s'
        if enableSave:
            logging.basicConfig(
                level=logging.INFO,
                format=self.loggerWrapperFormat,
                handlers=[
                    logging.FileHandler(nameFileForLogFile),
                    logging.StreamHandler(stream=sys.stdout),
                ],
                datefmt='%d-%m-%Y %H-%M-%S'
            )
        else:
            logging.basicConfig(
                level=logging.INFO,
                format=self.loggerWrapperFormat,
                datefmt='%d-%m-%Y %H-%M-%S'
            )
        self.logginWrapper = logging.getLogger()
        # ------- # Default attributes -> Path # ------- #

        # self.pathFileForLogFile = self.pathHome
    # ------- # Methods -> getSpaces # ------- #
    def getSpaces(self, maximumSpacesTypeInt: int, wordToCalcTypeStr: str):
        # init basic args
        lenWord = maximumSpacesTypeInt - int(len(str(wordToCalcTypeStr)))
        spacesToReturn = ' '*lenWord
        # return the spaces
        return spacesToReturn

    # ------- # Methods -> printLog # ------- #
    def printLog(
            self,
            logPrintTypeInt: int,
            msgTypeStr: str,
            statusInBracketTypeStr: str = False,
            colorToPickTypeInt: int = False,
    ):
        """
        - Flag :
            - dateEnableDisableTypeBool :
                - True == With date
                - False == Without date
            - logPrintTypeInt:
                - What will be inside the Status && what will be the color :
                    - 0 == info :           BlueColor            | Bold
                    - 1 == pass :           greenColor           | Bold
                    - 2 == failed :         failColor            | Bold
                    - 3 == check started :  yellowColor          | Bold
                    - 4 == check ended :    yellowColor          | Bold
                    - 5 == change :         turquoiseColor       | Bold
                    - 6 == ignoring :       yellowColor          | Bold
                    - 7 == User Need :      WhiteColor           | None
                    - 8 == init :           yellowColor          | Bold
                    - 9 == Activated :      WhiteColor           | Bold
                    - 10 == Checking :       yellowColor         | Bold
                    - 11 == Warning  :       yellowColor         | Bold
            - statusInBracketTypeStr:
                - What the status will be --> only work on level 7++
            - colorToPickTypeInt :
                - What color will be instert --> only work on level 7++ :
                    - 0 : white [default]
                    - 1 : blue
                    - 2 : red
                    - 3 : yellow
                    - 4 : turquoise
                    - 5 : green
        """
        # init basic Var
        status = ''
        colorToPick = ''
        boldText = self.makeBold
        separator = u'|'
        showResults = f'{msgTypeStr}'
        builder = ''
        currentTime = datetime.datetime.now().strftime(f"%d-%b-%y %T:%f")
        # assign the correct color and status --> info : blue : bold
        if logPrintTypeInt in list(range(0, 6)) or logPrintTypeInt in list(range(8, 12)):
            status = self.optionsLogger[logPrintTypeInt]['status']
            colorToPick = self.optionsLogger[logPrintTypeInt]['color']

        # assign the correct color and status --> user need
        elif logPrintTypeInt == 7:
            # check for status
            if statusInBracketTypeStr:
                status = f'[{statusInBracketTypeStr}]'

            # check for color
            if colorToPickTypeInt in list(range(1, 6)):
                colorToPick = self.optionsLogger[colorToPickTypeInt]['color']

        # formatter = coloredlogs.ColoredFormatter(self.loggerWrapperFormat)
        # logging.setFormatter(formatter)
        # self.logginWrapper.addHandler(self.logginWrapper)

        logging.addLevelName(logging.INFO, status)
        self.logginWrapper.info(
            f'{self.makeBold}{colorToPick}{msgTypeStr}{self.endOfLine}')
        # return

        return f'{currentTime} {separator}{status} {msgTypeStr}'
    # ------- # Methods -> printEmpty # ------- #
    def printNoFormat(self, msgTypeStr: str):
        """
        - Explain :
            - print without any color , just collect data for log
        """
        print(msgTypeStr)
    # ------- # Methods -> printColor # ------- #
    def printColor(self, colorToPickTypeInt: int, msgTypeStr: str, showPrint: bool = True, returnOutput: bool = False):
        """
        - Explain :
            - Print with any color and not with any item of printLog
        - Flags :
            - colorToPickTypeInt :
                - 0 : white [default]
                - 1 : blue
                - 2 : red
                - 3 : yellow
                - 4 : turquoise
                - 5 : green
            - msgTypeStr :
                - What do you want to print ?
        """
        global outputFileContantTypeList
        # init basic vars
        showResults = msgTypeStr
        colorToPick = ''
        # check for color
        # blue
        if colorToPickTypeInt in list(range(0, 6)):
            colorToPick = self.optionsLogger[colorToPickTypeInt]['color']
        showResults = f'{self.makeBold}{colorToPick}{showResults}{self.endOfLine}'
        # print the output
        # self.checkSavingLoggerStatus()
        return showResults


if __name__ == "__main__":
    pass
    log = logger(True)
    log.printLog(2, 'test')
    log.printLog(0, 'test')
