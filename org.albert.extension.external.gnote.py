#!/usr/bin/env python

""" A quick and dirty shim to search Gnote over dbus.
    Note: This does a full-text search on all of your notes for each keystroke, so it may introduce
    noticeable lag while searching if you have a lot of notes. As long as you use a trigger it
    won't affect your non-Gnote searches.
"""

from pydbus import SessionBus
import os
import sys
import json

albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata = {
        "iid": "org.albert.extension.external/v2.0",
        "name": "Gnote",
        "version": "0.1",
        "author": "Will Timpson",
        "dependencies": ["gnote", "python-pydbus"],
        "trigger": "gn "
    }
    print(json.dumps(metadata))
    sys.exit(0)

elif albert_op == "NAME":
    print("Gnote")
    sys.exit(0)

elif albert_op == "QUERY":
    def build_action(name, interface, arguments=None):
        action = {
            "name": name,
            "command": "dbus-send",
            "arguments": [
                "--type=method_call",
                "--dest=org.gnome.Gnote",
                "/org/gnome/Gnote/RemoteControl",
                "org.gnome.Gnote.RemoteControl.{}".format(interface)
            ]
        }
        if arguments:
            action['arguments'].append("string:{}".format(arguments))

        return action

    def build_item(id, name, actions):
        item = {
            "id": id,
            "name": name,
            "description": "Gnote",
            "icon": "gnote",
            "actions": actions
        }
        return item

    bus = SessionBus()
    gnote = bus.get("org.gnome.Gnote", "/org/gnome/Gnote/RemoteControl")
    query = ' '.join(os.environ.get("ALBERT_QUERY").split(' ')[1:])
    items = []

    note_actions = [
        ("Open Note", "DisplayNote"),
        ("Hide Note", "HideNote"),
        ("Delete Note", "DeleteNote")
    ]
    for note in gnote.SearchNotes(query, False):
        action_list = []
        for label, interface in note_actions:
            action_list.append(build_action(label, interface, note))

        items.append(build_item(note, gnote.GetNoteTitle(note), action_list))

    app_actions = [
        ("Create New Note", "CreateNote"),
        ("Display Search Window", "DisplaySearch")
    ]
    for label, interface in app_actions:
        action_list = [build_action(label, interface)]
        items.append(build_item(label, label, action_list))

    print(json.dumps({"items": items}))
    sys.exit(0)

else:
    sys.exit(0)
