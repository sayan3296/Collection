#!/usr/bin/env python

from __future__ import print_function
import os;
import sys;
import re;
from datetime import datetime;
from subprocess import Popen,PIPE,STDOUT;
from socket import gethostbyname;
from os import path

def runCmd(cmd):
    proc=Popen(cmd,stdout=PIPE,stderr=STDOUT)
    output, err=proc.communicate()
    return output.strip()
###
## example use
###rhel=runCmd(['cat','/etc/redhat-release'])

def runShellCmd(cmd):
    proc=Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=True)
    output, err =proc.communicate()
    return output.strip()

(system, node, release, version, machine) = os.uname();
rn_kern = 'kernel-' + release;
lt_kern = runShellCmd("/bin/rpm -q --last kernel | head -1 | awk '{print $1}'");
ptlvl = runShellCmd("cut -d':' -f1 /etc/ATTPatchlevel");
oskern = release.split('.x')[0];
check = [['3.10.0-693.17.1.el7','2.6.32-696.20.1.el6','2.6.18-426.el5','2Q2018'],
        ['3.10.0-693.2.2.el7','3.10.0-693.1.1.el7','2.6.32-696.10.3.el6','2.6.18-423.el5','4Q2017'],
        ['3.10.0-693.11.6.el7','3.10.0-693.11.1.el7','2.6.32-696.18.7.el6','2.6.32-696.16.1.el6','2.6.18-423.el5','1Q2018'],
        ['3.10.0-514.6.2.el7','2.6.32-642.16.1.el6','2.6.32-642.15.1.el6','2.6.18-419.el5','2Q2017']];
##

dirname = '/var/tmp/os_patch_val'
files = (
    'IP-Addr',
    'IP-Link',
    'Name-IP',
    'IP-Route',
    'FS-Mount'
)
errfilename = 'err'


def diff(check, f1, f2, errout=None):
    '''Diffing function'''

    lines = {}
    with open(f1) as f:
        lines[f1] = f.read().splitlines()
    with open(f2) as f:
        lines[f2] = f.read().splitlines()

    f1_extra = set(lines[f1]) - set(lines[f2])
    f2_extra = set(lines[f2]) - set(lines[f1])

    if len(f1_extra) == len(f2_extra) == 0:
        #print('* {:>10} check.....: successful'.format(check))
        print('->',check, "Check", ": Passed".rjust(30-len(check), '.'))
        # No difference
        return

    files_to_check = {}
    if len(f1_extra) > 0:
        # File 1 has extra lines
        files_to_check[f1] = f1_extra
    if len(f2_extra) > 0:
        # File 2 has extra lines
        files_to_check[f2] = f2_extra
#    print('{:>0} Check...............: Failed [ Check {} ]'.format(check, errout.name))
    print('->',check, "Check", ": Failed".rjust(30-len(check), '.') +' [ check ' + errout.name + ' ]')

    if errout is not None:
        errout.write('# {} check:\n\n'.format(check))
        for filename, extra in files_to_check.items():
            errout.write('### {}\n{}\n\n------------------\n'.format(
                filename,
                '\n'.join(['* Line {:3}: {}'.format(lines[filename].index(line), line) for line in extra])
            ))


## Kernel Check

if lt_kern == rn_kern:
        print ("-> Kernel Check.................: Passed " + "[ " + oskern + " ]")
else :
        print ("-> Kernel Check.................: Failed " + "[ " + "(L) " + lt_kern + " != (R) " + rn_kern + " ]")

## Patch Check

if ptlvl == '2Q2018' and oskern in check[0]:
        print ("-> Patch Check..................: Passed [ " + ptlvl + " --> " + oskern + " ]");
elif ptlvl == '4Q2017' and oskern in check[1]:
        print ("-> Patch Check..................: Passed [ " + ptlvl + " --> " + oskern + " ]");
elif ptlvl == '1Q2018' and oskern in check[2]:
        print ("-> Patch Check..................: Passed [ " + ptlvl + " --> " + oskern + " ]");
elif ptlvl == '2Q2017' and oskern in check[3]:
        print ("-> Patch Check..................: Passed [ " + ptlvl + " --> " + oskern + " ]");
else:
        print ("-> Patch Check..................: Failed [ " + ptlvl + " != " + oskern + " ]");

def precheck():
    '''Check if all files are there'''
    for file in files:
        file1 = path.join(dirname, 'pre_{}.out'.format(file))
        file2 = path.join(dirname, 'post_{}.out'.format(file))
        if not path.isfile(file1) or not path.isfile(file2):
            print('ERROR: {} check: pre or post check file is missing')
            quit()

def run():
    '''Run CLI'''
    errfile = path.join(dirname, '{}.out'.format(errfilename))
    with open(errfile, 'w') as f:
        for check in files:
            file1 = path.join(dirname, 'pre_{}.out'.format(check))
            file2 = path.join(dirname, 'post_{}.out'.format(check))
            diff(check, file1, file2, f)



if __name__ == '__main__':
    precheck()
    run()