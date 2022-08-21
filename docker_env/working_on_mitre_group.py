#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version_info__ = ('1','0','0')

#############################################
# written by thomas.billaut@protonmail.com  #
# date 7/21/22                              #
# source on github                          #
#############################################

import json
import re
import sys
from pprint import pprint
import attackcti
from sys import platform

if platform == 'linux' :
    out_dir = './out/'
elif platform == 'win32':
    out_dir = ".\\out\\"

def from_list_to_string(l):
    '''convert list of string as 1 unique string'''
    result = ""
    if len(l) > 0:
	    for item in l:
		    result = result + str(item) +", "
	    result = result[:-2]
    #print(result)
    return result


def write_group_as_paragraph(group,reg) :
    group_result = {}
    i = 1
	# 1 : (group as string, group aliases as string, group description as string )
    for d in group:
	    if "group_description" in d.keys():
		    if re.search(reg, d['group_description']):
				#print(group.index(d),d['group'], d['group_aliases'])
			    group_result[i] = (str(d['group']), from_list_to_string(d['group_aliases']), str(d['group_description']))
			    i += 1
    for item in group_result:
	    filename = out_dir + "c1_" + str(item) + ".txt"
	    desc = re.sub(pattern=r'\[([a-zA-Z0-9 ]+)\]', repl='\\1 ',string = group_result[item][2])
	    descf = re.sub(pattern=r'\((Citation:.*?)\)\s?([a-zA-Z0-9])', repl='(\\1)\n\n\\2',string = desc)
	    descff = re.sub(pattern=r'\((Citation:.*?)\)', repl='\n\\1',string = descf)
	    #descf = re.sub(pattern=r'\((Citation:.+?)\)', repl='\n\\1\n',string = desc)
	    result = group_result[item][0] + "\nAlias : " + group_result[item][1] + "\n\n" + descff + "\n"
	    with open(filename, "w") as f:
		    f.write(result)
	    f.close()
	    #print(result)
    return 0


def retrieve_group_tech(group,reg):
	''' retrieve threat actors ttps based on id'''
	group_list_item=[]
	lift = attackcti.attack_client()
	for d in group:
		if "group_description" in d.keys():
			if re.search(reg, d['group_description']):
				print(group.index(d),d['group'], d['group_aliases'])
				group_list_item.append(group.index(d))
	#print(group_list_item)
	dict_group = {}
	j = 1
	for i in group_list_item:
		print(("[+] - retrieving group %d")%(j))
		tech_by_group = []
		tech_by_group = lift.get_techniques_used_by_group(group[i],stix_format=False)
		dict_group[group[i]['group']] = tech_by_group
		j += 1
	result_file="mitre_group_" + reg + ".json"
	with open(result_file,"w") as file:
		file.write(json.dumps(dict_group))
	file.close()
	print("[+] - group retrieved finished")
	#print(dict_group)
	return 0


if __name__ == '__main__':
	reg = sys.argv[1]
	f = "mitre_group.json"
	group_list_item=[]
	with open(f,"r") as file:
		group = json.loads(file.read())
	file.close()
	print("[+] - starting")
	write_group_as_paragraph(group,reg)
	print("[+] - finished")