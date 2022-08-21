#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version_info__ = ('1','0','1')

#############################################
# written by thomas.billaut@protonmail.com  #
# date 7/21/22                              #
# source on github                          #
#############################################

from os import listdir
from os import chdir 
import argparse

def unicodeToAsciiff(inStr):
    ''' change u'\u2019':"'" and u'\u2018' latin-1 for latin-1 encoding '''
    result = ""
    for i in inStr:
        if i == u'\u2019':
            result += "'"
        elif i == u'\u2018':
            result += "`"
        else:
            result += i
    return result


def check_encoding(f):
    ''' check latin-1 character in a file and change it '''
    with open(f, "r") as myfile:
        s=myfile.read()
    myfile.close()
    s_m = unicodeToAsciiff(s)
    with open(f, "w") as myfile_m:
        myfile_m.write(s_m)
    myfile_m.close()

    
def clean(dir):
    '''list text file in directory and clean it'''
    file = listdir(chdir(dir))
    text_file = [ x for x in file if x.rfind(".txt")>0]
    for item in text_file:
        try :
            check_encoding(item)
        except Exception as e:
            print(e)
    chdir('../')


if __name__ == '__main__':
    __version__ = '.'.join(__version_info__)
    parser = argparse.ArgumentParser(description='tool for cleaning special unicode key for latin-1 printing in text directory')
    parser.add_argument("-dir", "--directory", action = "store", dest = "directory_to_clean", type=str, help="Give the directory name to clean\n")
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args()
    clean(".")



