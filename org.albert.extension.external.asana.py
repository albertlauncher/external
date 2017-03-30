#!/usr/bin/env python

# Created by Adam Gyulavari
# Install:
# - pip install asana
# - create an ENV var called ASANA_TOKEN with your personal Asana Token you can get from your profile settings
# - specify the asana_add.py path, if its not there
#
# Usage:
# as[-project_filter] task name
# Example:
# as dont forget the milk
# as-my wash car

import os
import sys
import json
import asana

asana_add_path = "/home/aze/.local/share/albert/external/asana_add.py"
asana_cache_file_path = "asana.ws"
token = os.environ.get("ASANA_TOKEN")
albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata="""{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Asana",
      "version":"1.0",
      "author":"Adam Gyulavari",
      "dependencies":[],
      "trigger":"as"
    }"""
    print(metadata)
    sys.exit(0)

elif albert_op == "NAME":
    print("Asana")
    sys.exit(0)

elif albert_op == "INITIALIZE":
    client = asana.Client.access_token(token)
    ws = list(client.workspaces.find_all())
    for w in ws:
        w['project'] = list(client.projects.find_all({"workspace": w['id']}))
    open(asana_cache_file_path, "w").write(json.dumps(ws))
    if client != None:
        sys.exit(0)
    else:
        sys.exit(1)

elif albert_op == "FINALIZE":
    sys.exit(0)

elif albert_op == "SETUPSESSION":
    sys.exit(0)

elif albert_op == "TEARDOWNSESSION":
    sys.exit(0)

elif albert_op == "QUERY":
    ws = json.loads(open(asana_cache_file_path, "r").read())
    albert_query = os.environ.get("ALBERT_QUERY")
    if len(albert_query) > 2 and albert_query[2] == "-":
        pq = albert_query[3:].split(" ")[0]
        q = " ".join(albert_query[3:].split(" ")[1:])
    else:
        pq = ""
        q = albert_query[3:]

    class Item(object):
        def __init__(self, wid, name, description, icon, projects):
            self.wid = wid
            self.name = name
            self.description = description
            self.icon = icon
            self.actions = []
            for p in projects:
                if pq in p['name'].lower():
                    self.actions.append({
                        "name": "Add to " + p['name'],
                        "command": "python",
                        "arguments": [asana_add_path, self.wid[3:], str(p['id']), q]
                    })

    items = []

    for w in ws:
        item = Item("as_"+str(w['id']), "Add Task to " + w['name'], "Add an Asana task: " + q, "vcs-added", w['project'])
        items.append(item)

    results = []
    for it in items:
        results += [json.dumps(it, default=lambda o: o.__dict__)]

    print('{"items": [' + ", ".join(results) + "]}")
    sys.exit(0)

elif albert_op == "COPYTOCLIPBOARD":
    sys.exit(0)
