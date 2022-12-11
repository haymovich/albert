#!/usr/bin/python3
"""
@Auther Name - Bar levi haymovch
@Auther Email - bar.rose65@gmail.com

<SCRIPT EXAPLAIN>
alb -bak -fp LICENSE -ibf
"""
import argparse
import os
import datetime
from logger import logger
from reader import Reader
# ------- # Outside Variable  - albert searcher # ------- #
scriptNickname = '-bak'
# ------- # Outside Variable - visual && usefull variable # ------- #
startTime = datetime.datetime.now()
log = logger(False)
# ------- # Outside Dynamic Variable - scipt args # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
# ------- # Outside function - configParser # ------- #
def configParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ibf", "--init_backup_file", help="init backup to file",   action='store_true',required=False, default=None)
    parser.add_argument("-fp", "--files_path", help="What the location for the file", nargs="+",required=False, default=False)
    return parser
# ------- # Class -> tamplateClass # ------- #
class BackupFiles():
    """
    - Exaplain :
        - Enable backup file/folder
    """
    def __init__(self):
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        self.nameAutoBackupName = 'bak'
        # ------- # Default attributes -> Path # ------- #
        self.pathToBackupFolder = Reader().extractorFilePathFromAlbertConfigFiles('bak')

    def renameItemToHaveDate(self,itemToRenameTypeStr:str):
        # init basic var
        _extantion = ''
        _itemNameRename = ''
        _itemToRenameTypeStr = itemToRenameTypeStr
        # _insertAutoDate = datetime.datetime.now().strftime(f"Date_%d-%m-%Y_Time_%H-%M-%S-%f")
        _insertAutoDate = datetime.datetime.now().strftime(f"Date_%d-%m-%Y")
        _fullName = ''
        try:
            _itemNameRename,_extantion = str(_itemToRenameTypeStr).split('.')
            _fullName = f'{_itemNameRename.strip()}_{_insertAutoDate}.{_extantion}'
            return _fullName
        except ValueError:
            _itemNameRename = str(_itemToRenameTypeStr).strip()
            _fullName = f'{_itemNameRename.strip()}_{_insertAutoDate}'
            return _fullName

    # ------- # Methods -> copyItemToBackupFolder # ------- #
    def copyItemToBackupFolder(self,itemLocationTypeStr:str,pathBackupFolderToCopyToTypeStr:str):
        # init basic var
        _itemLocationTypeStr = itemLocationTypeStr
        _pathBackupFolderToCopyToTypeStr = pathBackupFolderToCopyToTypeStr
        _pathToMovedItemToBackupFolder = os.path.join(_pathBackupFolderToCopyToTypeStr,os.path.basename(_itemLocationTypeStr))
        _itemNameRename = self.renameItemToHaveDate(_pathToMovedItemToBackupFolder)
        _command = ''
        # check if the item is exists
        if not os.path.exists(_itemLocationTypeStr):
            log.printLog(2,f'Item [{os.path.basename(_itemLocationTypeStr)}] does not exists , backup not started.')
        else:
            # check if the folder is exists 
            if not os.path.exists(_pathBackupFolderToCopyToTypeStr):
                _command = fr'sudo mkdir {_pathBackupFolderToCopyToTypeStr}'
                os.system(_command)
                log.printLog(1,f'Create folder backup [{os.path.basename(_pathBackupFolderToCopyToTypeStr)}]')
            # copy the item to the folder backup
            _command = f'sudo cp -r {_itemLocationTypeStr} {_pathBackupFolderToCopyToTypeStr}'
            os.system(_command)
            # rename this item
            _command = f'sudo mv {_pathToMovedItemToBackupFolder} {_itemNameRename}'
            os.system(_command)
            log.printLog(1,f'Item [{os.path.basename(_itemLocationTypeStr)}] Has succsfully copied to the backup folder.')
    
    # ------- # Methods -> initBackup # ------- #
    def initBackup(self,itemLocationTypeStr:str):
        # init basic var
        _itemLocationTypeStr = itemLocationTypeStr
        _extractBaseNameFromItem = os.path.basename(_itemLocationTypeStr).split('.')[0].strip()
        # name and path for generate item
        _nameGenerateBackupItem = f'{self.nameAutoBackupName}_{_extractBaseNameFromItem}'
        _pathGenerateBackupItem = os.path.join(self.pathToBackupFolder,_nameGenerateBackupItem)
        # init the backup method
        self.copyItemToBackupFolder(
            itemLocationTypeStr=_itemLocationTypeStr,
            pathBackupFolderToCopyToTypeStr=_pathGenerateBackupItem)
if __name__ == "__main__":
    args = configParser().parse_args()
    # ------- # Arguments -> -ibf -> init_backup_file # ------- #
    # ./backup.py -ibf -fp "<FILE_PATH_1>" "<FILE_PATH_2>"
    if args.init_backup_file:
        _filesPath = sorted(set(args.files_path))
        if _filesPath:
            _BackupFiles = BackupFiles()
            for _eachFileToCopy in _filesPath:
                _BackupFiles.initBackup(_eachFileToCopy)