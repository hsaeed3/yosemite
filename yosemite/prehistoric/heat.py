
"""
HEAT ~ hammad's extremely amplified toolkit

v~final out of 10000000 attempts
hopefully
"""


"""
hammock core now simplified
everything is now in one script
"""


import os
from colorama import Fore, Style
from pathlib import Path
import logging


"""
Radio

contains message functions for everything now
"""

class Radio:
    
    @staticmethod
    def success(message=None, arg=None):
        print(Fore.GREEN + f'[HKIT ~ SUCCESS] ' + Style.RESET_ALL + f'{Fore.GREEN + Style.BRIGHT}{message} {Fore.WHITE + Style.BRIGHT}{arg}' + Style.RESET_ALL if arg else Fore.GREEN + f'[SUCCESS] ' + Style.RESET_ALL + f'{Fore.GREEN + Style.BRIGHT}{message}' + Style.RESET_ALL)
        
    @staticmethod
    def warning(message=None, arg=None):
        print(Fore.LIGHTMAGENTA_EX + f'[HKIT ~ WARNING] ' + Style.RESET_ALL + f'{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}{message} {Fore.WHITE + Style.BRIGHT}{arg}' + Style.RESET_ALL if arg else Fore.LIGHTMAGENTA_EX + f'[WARNING] ' + Style.RESET_ALL + f'{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}{message}' + Style.RESET_ALL)
        
    @staticmethod
    def error(message=None, arg=None, etype=None):
        print(Fore.RED + f'[HKIT ~ ERROR] ' + Style.RESET_ALL + f'{Fore.RED + Style.BRIGHT}[{etype}] = {message} {Fore.WHITE + Style.BRIGHT}{arg}' + Style.RESET_ALL if arg and etype else Fore.RED + f'[ERROR] ' + Style.RESET_ALL + f'{Fore.RED + Style.BRIGHT}{message}' + Style.RESET_ALL)
        
    @staticmethod
    def status(message=None, arg=None):
        print(Fore.LIGHTYELLOW_EX + f'[HKIT ~ STATUS] ' + Style.RESET_ALL + f'{Fore.YELLOW + Style.DIM}{message} {Fore.WHITE + Style.DIM}{arg}' + Style.RESET_ALL if arg else Fore.LIGHTYELLOW_EX + f'[STATUS] ' + Style.RESET_ALL + f'{Fore.YELLOW + Style.DIM}{message}' + Style.RESET_ALL)
        
    @staticmethod
    def info(message=None, arg=None):
        print(Fore.LIGHTBLACK_EX + f'[HKIT ~ INFO] ' + Style.RESET_ALL + f'{Fore.LIGHTBLACK_EX + Style.BRIGHT}{message} {Fore.WHITE + Style.BRIGHT}{arg}' + Style.RESET_ALL if arg else Fore.LIGHTBLACK_EX + f'[INFO] ' + Style.RESET_ALL + f'{Fore.LIGHTBLACK_EX + Style.BRIGHT}{message}' + Style.RESET_ALL)
        

"""
CoreError 
"""

class CoreError(Exception):
    def __init__(self, message=None, arg=None):
        self.message = message
        
    def __str__(self):
        return f'{self.message}'
    
"""
CoreError ~ Types

usage:
    raise NoArg(arg)
    raise NoDir(arg)
    raise NoPath(arg)
    raise DoesNotExist(arg)
    raise InvalidDirectory(arg)
    raise InvalidFile(arg)
    raise InvalidExtension(arg)
    raise InvalidArgument(arg)
"""

class NoArg(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'NoArg'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify an argument for ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)
    

# Used if there is no directory provided
class NoDir(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'NoDir'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify a directory for ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)
    

# Used if there is no path provided
class NoPath(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'NoPath'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify a path for ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)


# Used if the path does not exist
class DoesNotExist(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'DoesNotExist'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify a real path for ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)


# Used if the directory is invalid
class InvalidDirectory(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'InvalidDirectory'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify a valid path for Directory ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)


# Used if the file is invalid
class InvalidFile(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'InvalidFile'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify a valid path for File ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)


# Used if the extension is invalid
class InvalidExtension(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'InvalidExtension'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify a valid extension for ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)


# Used if the argument is invalid
class InvalidArgument(CoreError):
    def __init__(self, arg = None, message = None):
        super().__init__(message)
        self.etype = 'InvalidArgument'
        self.arg = arg
        if not self.message:
            self.message = f'Please Specify a valid argument for ='
    
    def __str__(self):
        Radio.error(self.message, self.arg, self.etype)
    
"""
CoreLogger // Now Just Logger
"""

class Logger:
    def __init__(self, name, log_dir='logs', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
        file_handler.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, level, msg, *args, **kwargs):
        colored_msg = Fore.LIGHTBLACK_EX + f'{msg} ' + Fore.LIGHTCYAN_EX + f'{args}' + Style.RESET_ALL
        self.logger.log(level, colored_msg, *args, **kwargs)  
        

"""
CoreTools ~ Now also added here
"""

def dir_exist(directory: str = None) -> bool:
    
    if not directory:
        raise NoDir(arg='directory', message=None)
    directory = Path(directory)
    if not directory.exists():
        raise DoesNotExist(arg=directory, message=None)
    if not directory.is_dir():
        raise InvalidDirectory(arg=directory, message=None)
    return str(directory)

def file_exist(path: str = None) -> bool:
    
    if not path:
        raise NoPath(arg='path', message=None)
    path = Path(path)
    if not path.exists():
        raise DoesNotExist(arg=path, message=None)
    if not path.is_file():
        raise InvalidFile(arg=path, message=None)
    return str(path)

def spec_file(path: str = None, ext: str = None) -> bool:
    
    file_path = file_exist(path)
    file_path = Path(file_path)
    if file_path.suffix != ext:
        raise InvalidExtension(arg=file_path, message=f'Please Verify Your File Ends With [{ext}] @')
    path = str(file_path)
    return path


"""
Finally, Hammock Core
"""

class Core:
    
    """
    File / Directory Verification
    """
    
    def dir(directory: str = None) -> bool:
        
        Radio.status(message='Verifying Directory @', arg=directory)
        if dir_exist(directory):
            Radio.success(message='Directory Verified @', arg=directory)
            return directory
        else:
            pass
        
    def file(path: str = None) -> bool:
        
        Radio.status(message='Verifying File @', arg=path)
        if file_exist(path):
            Radio.success(message='File Verified @', arg=path)
            return path
        else:
            pass
        
    def ext(path: str = None, ext: str = None) -> bool:
        
        Radio.status(message='Verifying File Extension @', arg=path)
        if spec_file(path, ext):
            Radio.success(message='File Extension Verified @', arg=path)
            return path
        else:
            pass
        

if __name__ == '__main__':
    
    try:
        Core.dir(directory='/Users/hammad/Desktop/dev/hamlib/core')
        Core.file(path='/Users/hammad/Desktop/dev/hamlib/core/nucleus/__init__.py')
        Core.ext(path='/Users/hammad/Desktop/dev/hamlib/core/nucleus/__init__.py', ext='.py')
    except Exception as e:
        raise CoreError(e)