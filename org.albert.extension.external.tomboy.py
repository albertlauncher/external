#!/usr/bin/env python

""" A quick and dirty shim to search Tomboy Notes over dbus.
    Note: This does a full-text search on all of your notes for each keystroke, so you may want
    to add a trigger if you have a lot of notes.
"""

from pydbus import SessionBus
import os
import sys
import json

albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata="""{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Tomboy",
      "version":"0.1",
      "author":"Will Timpson",
      "dependencies":["tomboy", "python-dbus"],
      "trigger":""
    }"""
    print(metadata)
    sys.exit(0)

elif albert_op == "NAME":
    print("Tomboy")
    sys.exit(0)

elif albert_op == "QUERY":

    bus = SessionBus()
    tomboy = bus.get("org.gnome.Tomboy", "/org/gnome/Tomboy/RemoteControl")
    albert_query = os.environ.get("ALBERT_QUERY")

    items = []
    for note in tomboy.SearchNotes(albert_query, False):
        item = {"id": note,
                "name": tomboy.GetNoteTitle(note),
                "Description": "Tomboy Note",
                "icon": "tomboy",
                "actions": [{
                    "name": "Open Note",
                    "command": "tomboy",
                    "arguments": ["--open-note", note]
                    }]
                }
        items.append(item)

    print(json.dumps({"items": items}))
    sys.exit(0)

else:
    sys.exit(0)
