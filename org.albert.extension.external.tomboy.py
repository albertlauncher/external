#!/usr/bin/env python

""" A quick and dirty shim to search Tomboy Notes over dbus.
    Note: This does a full-text search on all of your notes for each keystroke, so it may introduce
    noticeable lag while searching if you have a lot of notes. As long as you use a trigger it
    won't affect your non-Tomboy searches.
"""

from pydbus import SessionBus
import os
import sys
import json

albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata="""{
        "iid": "org.albert.extension.external/v2.0",
        "name": "Tomboy",
        "version": "0.1",
        "author": "Will Timpson",
        "dependencies": ["tomboy", "python-pydbus"],
        "trigger": "tb "
    }"""
    print(metadata)
    sys.exit(0)

elif albert_op == "NAME":
    print("Tomboy")
    sys.exit(0)

elif albert_op == "QUERY":

    bus = SessionBus()
    tomboy = bus.get("org.gnome.Tomboy", "/org/gnome/Tomboy/RemoteControl")
    query = ' '.join(os.environ.get("ALBERT_QUERY").split(' ')[1:])

    items = []
    actions = {
        "Open Note": "org.gnome.Tomboy.RemoteControl.DisplayNote",
        "Hide Note": "org.gnome.Tomboy.RemoteControl.HideNote",
        "Delete Note": "org.gnome.Tomboy.RemoteControl.DeleteNote"
    }
    for note in tomboy.SearchNotes(query, False):
        action_list = []
        for label, interface in actions.items():
            action_list.append({
                "name": label,
                "command": "dbus-send",
                "arguments": [
                    "--type=method_call",
                    "--dest=org.gnome.Tomboy",
                    "/org/gnome/Tomboy/RemoteControl",
                    interface,
                    "string:{}".format(note)
                ]
            })

        item = {
            "id": note,
            "name": tomboy.GetNoteTitle(note),
            "description": "Tomboy Note",
            "icon": "tomboy",
            "actions": action_list
        }
        items.append(item)

    print(json.dumps({"items": items}))
    sys.exit(0)

else:
    sys.exit(0)
