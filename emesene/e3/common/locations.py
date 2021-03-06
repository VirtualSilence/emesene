'''a module that provides access to common locations'''
import os
import sys
import re
import subprocess

def downloads():
    '''
    return the location of the user's downloads folder

    on windows and mac os x return the desktop folder path
    '''

    if sys.platform.startswith('win'): # Windows
        from win32com.shell import shell, shellcon
        return shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
    elif sys.platform.startswith('darwin'): # Mac OS X
        return os.path.expanduser('~/Desktop')
    else: # Linux
        path = os.environ.get("XDG_DOWNLOAD_DIR") or \
            get_command_output("xdg-user-dir", "DOWNLOAD")

        if path is not None:
            return path

        downloads = join_home("Downloads")

        if os.path.isdir(downloads):
            return downloads

        else:
            return join_home()

def get_command_output(*args):
    '''
    run a command in the system and return the output,
    return None if something fails
    '''
    try:
        return subprocess.Popen(args,
                stdout=subprocess.PIPE).communicate()[0].strip()
    except OSError:
        return None

def get_from_user_dirs(name="XDG_DOWNLOAD_DIR"):
    '''
    get the value of *name* from user-dirs.dirs if exist and defined
    return None if not found
    '''

    user_dirs = os.path.expanduser('~/.config/user-dirs.dirs')

    if os.path.exists(user_dirs):
        match = re.search(name + '="(.*?)"',
                    open(user_dirs).read())
        if match:
            return os.path.expanduser(
                match.group(1).replace('$HOME', '~'))

    return None

def join_home(*paths):
    '''
    join the list of strings to the home folder

    return Nont if $HOME is not set expand ~ fails and xdg-user-dir doesn't exist (?)
    '''

    home = os.environ.get("HOME") or os.path.expanduser("~") or \
            get_command_output("xdg-user-dir")

    if home is None:
        return None

    return os.path.join(home, *paths)
