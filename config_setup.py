#/usr/bin/python3

import sys
import argparse
from fabric.api import execute, run, env
from fabric.context_managers import settings
from fabric.main import load_fabfile
from fabric.main import state

"""
Available commands we support.
TODO:
    1)  amend these to save the output in a string and
        return only the needed output
    2)  do some error checking. For example, some of the
        commands may not be existent on particular OSs
"""
def get_kernel_name():
    run('uname -s', shell=False)

def get_kernel_release():
    run('uname -r', shell=False)

def get_kernel_version():
    run('uname -v', shell=False)# stdout=yo, stderr=yo)

def get_arch():
    run('uname -m', shell=False)

def get_os():
    run('uname -o', shell=False)

def main():
    #setup here argument parser
    parser = argparse.ArgumentParser(description='configure remote server')
    parser.add_argument('--hostname', default='localhost', help='Hostname of server')
    parser.add_argument('-u', '--username', help='Username to use for login')
    parser.add_argument('--kernel-version', dest='commands', action='append_const', const=get_kernel_version)
    parser.add_argument('--kernel-release', dest='commands', action='append_const', const=get_kernel_release)
    args = parser.parse_args()
    #print(args)

    """
    Setup the url of the server
    """
    if args.username is not None:
        host_string = "{0}@{1}".format(args.username, args.hostname)
    else:
        host_string = args.hostname

    """
    Run all the user-defined commands
    """
    with settings(host_string=host_string, warn_only=True):
        for cmd in args.commands:
            cmd()

main()
