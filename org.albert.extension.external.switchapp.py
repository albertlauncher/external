#!/usr/bin/env python

import subprocess
import sys
import re
import os
import json

albert_op = os.environ.get('ALBERT_OP')

if albert_op == 'METADATA':
    metadata = """{
    "iid": "org.albert.extension.external/v2.0",
    "name": "WindowSwitcher",
    "version": "1.0",
    "author": "Klesh Wong",
    "dependencies": [],
    "trigger": "`"
    }"""
    print(metadata)
    sys.exit(0)
elif albert_op == 'QUERY':
    albert_query = os.environ.get('ALBERT_QUERY')
    if albert_query:
        albert_query = albert_query[1:]

    process = subprocess.Popen(['wmctrl', '-l'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print error
        sys.exit(1)
    items = []
    patt = re.compile(r'^(\w+)\s+(\d+)\s+(\S+)\s+(.+)$')
    for line in output.split('\n'):
        match = patt.match(line)
        if not match:
            continue

        name = match.group(4)

        if albert_query and albert_query.lower() not in name.lower():
            continue

        item = {
            'id' : match.group(1),
            'name' : name,
            'actions' : [{
                'name': 'Activiate',
                'command': 'python',
                'arguments': [
                    __file__,
                    str(match.group(1))
                ]
            }]
        }

        items.append(item)

    resp = {
        'items' : items
    }
    text = json.dumps(resp)
    print(text)


if len(sys.argv) > 1:
    window_id = sys.argv[1]
    subprocess.Popen(['wmctrl', '-ia', window_id])
