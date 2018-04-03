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
def get_routing_table():
    run('show ip route', shell=False)

def get_routing_protocols():
    run('show ip protocols', shell=False)

def get_cdp_neighbours():
    run('show cdp neighbours', shell=False)# stdout=yo, stderr=yo)

def get_arch():
    run('uname -m', shell=False)

def get_os():
    run('uname -o', shell=False)

def main():
    #setup here argument parser
    parser = argparse.ArgumentParser(description='configure remote server')
    parser.add_argument('--hostname', default='localhost', help='Hostname of server')
    parser.add_argument('-u', '--username', help='Username to use for login')
    parser.add_argument('--routing-table', dest='commands', action='append_const', const=get_routing_table)
    parser.add_argument('--cdp-neighbours', dest='commands', action='append_const', const=get_cdp_neighbours)
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
