#!/usr/bin/env python

import os
import sys
import json
import commands
from ConfigParser import SafeConfigParser

"""

A quick window switcher

required: wmctrl

"""

albert_op = os.environ.get("ALBERT_OP")

APPLICATIONS_DIR = "/usr/share/applications/"

if albert_op == "METADATA":
    metadata={
      "iid":"org.albert.extension.external/v2.0",
      "name":"Switcher",
      "version":"0.1",
      "author":"Airking05",
      "dependencies":[],
      "trigger":","
    }
    print(json.dumps(metadata))
    sys.exit(0)

elif albert_op == "NAME":
    print("Switcher")
    sys.exit(0)

elif albert_op == "INITIALIZE":
    if not commands.getstatusoutput("which wmctrl")[0] is 0:
        sys.exit(1)
    sys.exit(0)

elif albert_op == "QUERY":
    def build_action(name):
        action = {
            "name": "switch to %s"%name,
            "command": "wmctrl",
            "arguments": ["-a",name]
        }
        return action

    def build_item(id,name,icon,description,actions):
        item = {
            "id": id,
            "name": name,
            "description": description,
            "completion": "switched",
            "icon": icon,
            "actions": actions
        }
        return item

    albert_query = "".join(os.environ.get("ALBERT_QUERY").split(",")[1:])
    window_list = commands.getoutput("wmctrl -l -x").split("\n")
    items = []

    for window_row in window_list:
        action_list = []
        window = window_row.split()
        window_program = window[2].split(".")[0]
        window_title = "".join(window[4:])
        window_text = window_program + '' + window_title
        config_file = APPLICATIONS_DIR + window_program + ".desktop"
        if albert_query == "" or albert_query in window_text.lower():
            if not os.path.exists(config_file):
                name = window_program
                icon = "utilities-terminal"
                description = window_title
            else:
                parser = SafeConfigParser()
                parser.read(config_file)
                name = parser.get("Desktop Entry","Name")
                icon = parser.get("Desktop Entry","Icon")
                description = window_title

            id = window[0]
            action_list.append(build_action(name))
            items.append(build_item(id,name,icon,description,action_list))

    print(json.dumps({"items":items}))
    sys.exit(0)

elif albert_op in ["FINALIZE", "SETUPSESSION", "TEARDOWNSESSION"]:
    sys.exit(0)
