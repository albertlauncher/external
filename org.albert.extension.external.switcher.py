#!/usr/bin/env python

import os
import sys
import json
import commands

"""

A quick window switcher

required: wmctrl

"""

albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata="""{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Switcher",
      "version":"0.1",
      "author":"Airking05",
      "dependencies":[],
      "trigger":"sw "
    }"""
    print(metadata)
    sys.exit(0)

elif albert_op == "NAME":
    print("Switcher")
    sys.exit(0)
    
elif albert_op == "QUERY":
    def build_action(name,interface,arguments=None):
        action = {
            "name": "switch to %s"%name,
            "command": "wmctrl",
            "arguments": ["-a",arguments]
        }
        return action
    
    def build_item(id,name,actions):
        item = {
            "id": id,
            "name": name,
            "description": "Switcher",
            "icon": "",
            "actions": actions
            
        }
        return item
    
    albert_query = os.environ.get("ALBERT_QUERY")
    window_list = commands.getoutput("wmctrl -l -x").split("\n")
    items = []
    for window_row in window_list:
        window = window_row.split()
        action_list = []
        name = (window[2].split("."))[-1]
        id = window[0]
        action_list.append(build_action(name,False,window[-1]))
        items.append(build_item(id,name,action_list))
        
    print(json.dumps({"items":items}))
    sys.exit(0)
    
elif albert_op in ["INITIALIZE", "FINALIZE", "SETUPSESSION", "TEARDOWNSESSION"]:
    sys.exit(0)
