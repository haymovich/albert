#!/usr/bin/python3
import sys
import os
import datetime
import subprocess
import argparse
from reader import Reader
from logger import logger
"""
Author@Bar Levi Haymovich
"""
# ------- # Outside Variable  - con searcher # ------- #
scriptNickname = '-git'
# ------- # Outside Variable - visual && usefull variable # ------- #
log = logger(False)
# ------- # Outside function - configParser # ------- #
def configParser():
    """
    """
    parser = argparse.ArgumentParser()
    possibleOptionToNewTag = ['1', '2', '3']
    parser.add_argument(
        "-p", "--push", help="push to repo , no password required", action='store_true', default=None)
    parser.add_argument("-s", "--sentence", nargs='+',
                        help="What to write in the push/new tag.", default=None)
    parser.add_argument(
        "-nt", "--new_tag", help="release new tag - option [1-Majot/2-Minor/3-Patch]", choices=possibleOptionToNewTag, default=None)
    parser.add_argument("-gtf", "--go_to_folder",
                        help="When releasing to git , which folder to relelase ?", default=os.getcwd())
    parser.add_argument("-t", "--testing", help=argparse.SUPPRESS,
                        action='store_true', required=False, default=False)
    return parser


# ------- # global -> outside function # ------- #
# ------- # global function -> checkOsSystem # ------- #
# ------- # global -> outside variable # ------- #
scriptName = os.path.basename(__file__)


# ------- # Class -> GitHubManager # ------- #
class GitHubManager:
    """
    - Explain :
        - Github manager that can :
            - auto basic flow for :
                - git add .
                - git commit -m "InsertMessage"
                - git push
    """

    def __init__(self):
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #
        pass

    # ------- # Methods -> pushBasicToGithub # ------- #
    def sendCommandToTerminalAndGetOutpout(self, commandToSendTypeStr: str):
        """
        - Explain :
            - Send any command to terminal and return in to user as return .
        - Flag :
            - commandToSendTypeStr
                - Which command to send
        - Return:
            - return the command as is.
        """
        # work flow
        newCommandSplitter = commandToSendTypeStr.split(' ')

        return subprocess.check_output(newCommandSplitter)

 # ------- # Methods -> pushBasicToGithub # ------- #
    def getLatestTagReleaseFromGit(self):
        """
        - Explain :
            - Get the latest tag from git and release it with update.
        - Flag :
            - None
        - Return:
            - If there none any tag then add the tag to auto add tag
        """
        # work flow
        try:
            extractReleaseTag = self.sendCommandToTerminalAndGetOutpout(
                'git describe')
            if 'False' in str(extractReleaseTag):
                return 'v1.0.0'
            else:
                return str(extractReleaseTag)[2::].split('-')[0]

        except subprocess.CalledProcessError:
            log.printLog(0,'Auto tag has been enable , tag 1.0.0 is create now for project.')
            return False

     # ------- # Methods -> pushBasicToGithub # ------- #
    def pushBasicToGithub(self, msgToCommitTypeStr: str):
        """
        - Explain :
            - push changes to git without any flows
        - Flag :
            - msgToCommitTypeStr : str
                - What to release for github.
        - Return:
            - call the update for insert message
        """
        # work flow.
        getLatesTag = ''
        if self.getLatestTagReleaseFromGit():
            getLatesTag = str(self.getLatestTagReleaseFromGit()
                              ).replace('\n', '').replace('\\n', '').replace("'", '')
        else:
            # enable create auto tag
            getLatesTag = 'v1.0.0'
            self.createAutoTagToGit(
                setenceToReleaseTypeStr='', createAutoTagWhenNoTagInGit=True)
        # ragult push to git
        subprocess.call(["git", "add", "."])
        subprocess.call(
            ["git", "commit", "-m", f"LRT : [{getLatesTag}] | {msgToCommitTypeStr}"])
        subprocess.call(["git", "push"])

     # ------- # Methods -> createAutoTagToGit # ------- #
    def createAutoTagToGit(
            self,
            setenceToReleaseTypeStr: str,
            updateRevistionTypeStr: str = '3',
            tagVersion=False,
            createAutoTagWhenNoTagInGit=False
    ):
        """
        - Explain :
            - release to git with basic flow
        - Flag :
            - setenceToReleaseTypeStr
                - What should be in the release ?
            - tagVersion
                - This auto tag version is
        - Return:
            - call the update for insert message.
        """
        # check if needed to release tag without any iteration of the user
        if createAutoTagWhenNoTagInGit:
            # push any changes to git
            autoMesageToGit = f'Auto Release was create by adam framework - Date {datetime.datetime.now().strftime("%D %T")}'
            subprocess.call(
                ["git", "tag", "-a", "-m", f"{autoMesageToGit}", f"v1.0.0"])
            subprocess.call(["git", "push", "origin", f"--tags"])
            self.pushBasicToGithub('Auto Tag has been release.')
        else:
            getLatestRelease = ''
            if self.getLatestTagReleaseFromGit():
                getLatestRelease = str(
                    self.getLatestTagReleaseFromGit()).replace('v', '').replace('\\n', '').replace("'", '').split('.')

                firstIndex = int(getLatestRelease[0])
                secondIndex = int(getLatestRelease[1])
                thirdIndex = int(getLatestRelease[2])
                # first index
                if updateRevistionTypeStr == '1':
                    firstIndex += 1
                    thirdIndex = 0
                    secondIndex = 0
                # second index
                if updateRevistionTypeStr == '2':
                    secondIndex += 1
                    thirdIndex = 0
                # third index
                if updateRevistionTypeStr == '3':
                    thirdIndex += 1
                else:
                    thirdIndex += 1
                # init full release version
                tagVersion = f'v{firstIndex}.{secondIndex}.{thirdIndex}'
            else:
                tagVersion = 'v1.0.0'
            # Create auto tag to git
            subprocess.call(
                ["git", "tag", "-a", "-m", f"{setenceToReleaseTypeStr}", f"{tagVersion}"])
            subprocess.call(["git", "push", "origin", f"--tags"])
            self.pushBasicToGithub(
                f'{setenceToReleaseTypeStr}')


# Running only if system in this file
if __name__ == '__main__':
    args = configParser().parse_args()
    # check if git inside the current folder
    _folderToSearchTheGitFolder = args.go_to_folder
    if [i for i in ['albert_src','alb_src'] if i == _folderToSearchTheGitFolder]:
        _folderToSearchTheGitFolder = Reader().extractorFilePathFromAlbertConfigFiles('albert')
    os.chdir(_folderToSearchTheGitFolder)
    log.printLog(0,
        f'Try to search .git folder inside --> {_folderToSearchTheGitFolder}')
    if '.git' in os.listdir(_folderToSearchTheGitFolder):
        log.printLog(1,f'.git folder match --> {_folderToSearchTheGitFolder}')
        # init basic var
        # ------- # Arguments -> -s-> sentence # ------- #
        try:
            _sentence = ' '.join(args.sentence)
            # ------- # Arguments -> -p -> push # ------- #
            if args.push:
                # push basic stuff to git
                GitHubManager().pushBasicToGithub(_sentence)
            # ------- # Arguments -> -nt -> new_tag # ------- #
            elif args.new_tag:
                if str(args.new_tag) == str('1'):
                    log.printLog(7,'Init activated MAJOR release.','Major-Update',4)
                if str(args.new_tag) == str('2'):
                    log.printLog(7,'Init activated MINOR release.','Minor-Update',4)
                if str(args.new_tag) == str('3'):
                    log.printLog(7,'Init activated PATCH release.','Path-Update',4)
                GitHubManager().createAutoTagToGit(setenceToReleaseTypeStr=_sentence,
                                                   updateRevistionTypeStr=args.new_tag,)
        except TypeError:
            log.printLog(2,'Sentece was not giving , please insert a sentence.')
    # git folder not exists in the folder
    else:
        log.printLog(2, f'git repo folder is not in folder [{_folderToSearchTheGitFolder}] ,Try to run git clone and start again.')
  