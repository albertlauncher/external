#!/usr/bin/env python

""" A quick and dirty shim to search Tomboy Notes over dbus."""

import os
import sys
import json

from pydbus import SessionBus

bus = SessionBus()
tomboy = bus.get("org.gnome.Tomboy", "/org/gnome/Tomboy/RemoteControl")
albert_op = os.environ.get("ALBERT_OP")

if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        response = getattr(tomboy, sys.argv[1])(sys.argv[2])
    else:
        response = getattr(tomboy, sys.argv[1])()
    if sys.argv[1] == "CreateNote":
        tomboy.DisplayNote(response)

if albert_op == "METADATA":
    metadata = {
        "iid": "org.albert.extension.external/v2.0",
        "name": "Tomboy",
        "version": "0.1",
        "author": "Will Timpson",
        "dependencies": ["tomboy", "python-pydbus"],
        "trigger": "tb "
    }
    print(json.dumps(metadata))
    sys.exit(0)

elif albert_op == "QUERY":
    def build_action(name, interface, arguments=None):
        action = {
            "name": name,
            "command": sys.argv[0],
            "arguments": [interface]
        }
        if arguments:
            action['arguments'].append(arguments)

        return action

    def build_item(id, name, actions):
        item = {
            "id": id,
            "name": name,
            "description": "Tomboy Notes",
            "icon": "tomboy",
            "actions": actions
        }
        return item

    query = ' '.join(os.environ.get("ALBERT_QUERY").split(' ')[1:])
    items = []

    note_actions = [
        ("Open Note", "DisplayNote"),
        ("Hide Note", "HideNote"),
        ("Delete Note", "DeleteNote")
    ]
    for note in tomboy.SearchNotes(query, False):
        action_list = []
        for label, interface in note_actions:
            action_list.append(build_action(label, interface, note))

        items.append(build_item(note, tomboy.GetNoteTitle(note), action_list))

    app_actions = [
        ("Create New Note", "CreateNote"),
        ("Display Search Window", "DisplaySearch")
    ]
    for label, interface in app_actions:
        action_list = [build_action(label, interface)]
        items.append(build_item(label, label, action_list))

    print(json.dumps({"items": items}))
    sys.exit(0)

elif albert_op in ["INITIALIZE", "FINALIZE", "SETUPSESSION", "TEARDOWNSESSION"]:
    sys.exit(0)
