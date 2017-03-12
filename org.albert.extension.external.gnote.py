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
    metadata="""{
        "iid": "org.albert.extension.external/v2.0",
        "name": "Gnote",
        "version": "0.1",
        "author": "Will Timpson",
        "dependencies": ["gnote", "python-pydbus"],
        "trigger": "gn "
    }"""
    print(metadata)
    sys.exit(0)

elif albert_op == "NAME":
    print("Gnote")
    sys.exit(0)

elif albert_op == "QUERY":
    def build_action(label, interface, string=None):
        action = {
            "name": label,
            "command": "dbus-send",
            "arguments": [
                "--type=method_call",
                "--dest=org.gnome.Gnote",
                "/org/gnome/Gnote/RemoteControl",
                interface
            ]
        }
        if string:
            action['arguments'].append("string:{}".format(string))

        return action

    def build_item(id, title, actions):
        item = {
            "id": id,
            "name": title,
            "description": "Gnote",
            "icon": "gnote",
            "actions": actions
        }
        return item

    bus = SessionBus()
    gnote = bus.get("org.gnome.Gnote", "/org/gnome/Gnote/RemoteControl")
    query = ' '.join(os.environ.get("ALBERT_QUERY").split(' ')[1:])
    items = []

    note_actions = {
        "Open Note": "org.gnome.Gnote.RemoteControl.DisplayNote",
        "Hide Note": "org.gnome.Gnote.RemoteControl.HideNote",
        "Delete Note": "org.gnome.Gnote.RemoteControl.DeleteNote"
    }
    for note in gnote.SearchNotes(query, False):
        action_list = []
        for label, interface in note_actions.items():
            action_list.append(build_action(label, interface, note))

        items.append(build_item(note, gnote.GetNoteTitle(note), action_list))

    app_actions = [
        ("Create New Note", "org.gnome.Gnote.RemoteControl.CreateNote", None),
        ("Display Search Window", "org.gnome.Gnote.RemoteControl.DisplaySearch", None)
    ]
    for app in app_actions:
        label, interface, string = app
        action_list = [build_action(label, interface)]
        items.append(build_item(label, label, action_list))

    print(json.dumps({"items": items}))
    sys.exit(0)

else:
    sys.exit(0)
