#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version_info__ = ('1','0','0')

#############################################
# written by thomas.billaut@protonmail.com  #
# date 7/21/22                              #
# source on github                          #
#############################################

import json
import attackcti
import requests
import yaml


def get_group():
    """retrieve mitre group group from att&ck and save it as json file object"""
    lift = attackcti.attack_client()
    group = lift.get_enterprise_groups(stix_format=False)
    with open("mitre_group.json","w") as f: 
        f.write(json.dumps(group))
    f.close()
    return 0


def get_ossem_data():
    """retrieve ossem data"""
    # OLD out of date 
    #url = 'https://raw.githubusercontent.com/OTRF/OSSEM-DM/main/use-cases/mitre_attack/techniques_to_events_mapping.yaml'
    url= 'https://raw.githubusercontent.com/OTRF/OSSEM-DM/main/use-cases/mitre_attack/techniques_to_events_mapping.json'
    content = requests.get(url)
    y = content.text
    with open("techniques_to_events_mapping.yaml", "w") as f1:
        f1.write(y)
    f1.close
    return 0


if __name__ == '__main__':
    get_group()
    get_ossem_data()


    