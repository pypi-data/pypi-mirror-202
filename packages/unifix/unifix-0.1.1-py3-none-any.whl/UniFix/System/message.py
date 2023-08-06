'''
Add system message
'''
import os
import subprocess

def _get_sub_dirs(parent):
    """Returns a list of the child directories of the given parent directory"""
    return [child for child in os.listdir(parent) if os.path.isdir(os.path.join(parent, child))]

def _get_sub_files(parent):
    """Returns a list of the child files of the given parent directory"""
    return [child for child in os.listdir(parent) if os.path.isfile(os.path.join(parent, child))]

def get_sub_dirs(parent):
    '''Returns a sentence about the child directories of the given parent directory
        format: Directories: ...,...
    '''
    if not _get_sub_dirs(parent):
        return "There's no directory in the current path."
    dir = "Directories in the current directory:"
    for child in _get_sub_dirs(parent):
        dir += " " + child + ","
    dir = dir[:-1] + "."
    return dir

def get_sub_files(parent):
    '''Returns a sentence about the child files of the given parent directory
        format: Files: ...,...
    '''
    if not _get_sub_dirs(parent):
        return "There's no file in the current path."
    file = "Files in the current directory:"
    for child in _get_sub_files(parent):
        file += " " + child + ","
    file = file[:-1] + "."
    return file

def _get_branches():
    proc = subprocess.Popen(
        ['git', 'branch', '-a', '--no-color', '--no-column'],
        stdout=subprocess.PIPE, stderr= subprocess.DEVNULL)
    for line in proc.stdout.readlines():
        line = line.decode('utf-8')
        if '->' in line:    # Remote HEAD like b'  remotes/origin/HEAD -> origin/master'
            continue
        if line.startswith('*'):
            line = line.split(' ')[1]
        if line.strip().startswith('remotes/'):
            line = '/'.join(line.split('/')[2:])
        yield line.strip()

def get_branches():
    '''Returns a sentence about the child files of the given parent directory
        format: branches of git: ...,...
    '''
    branch_list = list(_get_branches())
    if not branch_list:
        return "There's no branch of git."
    branch = "Branches of git:"
    for child in branch_list:
        branch += " " + child + ","
    branch = branch[:-1] + "."
    return branch