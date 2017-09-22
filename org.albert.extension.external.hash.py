#!/usr/bin/env python
import hashlib
import json
import os
import sys


class Object(object):
    pass

def sha1Item(srcStr):
    sha1Str = hashlib.sha1(srcStr).hexdigest()

    item = Object()
    item.id = "hash-sha1"
    item.name = "sha1"
    item.description = "{0}".format(sha1Str)
    item.icon = ""
    item.actions = []

    action = Object()
    action.command = "sh"
    action.name = "copy to clipboard"
    action.arguments = ["-c", 'echo -n "{0}" | xclip -i -selection clipboard;'.format(sha1Str)]
    item.actions.append(action)
    return item


def sha224Item(srcStr):
    sha1Str = hashlib.sha224(srcStr).hexdigest()

    item = Object()
    item.id = "hash-sha224"
    item.name = "sha224"
    item.description = "{0}".format(sha1Str)
    item.icon = ""
    item.actions = []

    action = Object()
    action.command = "sh"
    action.name = "copy to clipboard"
    action.arguments = ["-c", 'echo -n "{0}" | xclip -i -selection clipboard;'.format(sha1Str)]
    item.actions.append(action)
    return item


def md5Item(srcStr):
    md5Str = hashlib.md5(srcStr).hexdigest()

    item = Object()
    item.id = "hash-md5"
    item.name = "md5"
    item.description = "{0}".format(md5Str)
    item.icon = ""
    item.actions = []

    action = Object()
    action.command = "sh"
    action.name = "copy to clipboard"
    action.arguments = ["-c", 'echo -n "{0}" | xclip -i -selection clipboard;'.format(md5Str)]
    item.actions.append(action)
    return item


albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata = Object()
    metadata.iid = "org.albert.extension.external/v2.0"
    metadata.name = "hash"
    metadata.version = "1.0"
    metadata.author = "glight2000"
    metadata.dependencies = []
    metadata.trigger = "hash"
    print(json.dumps(metadata, default=lambda o: o.__dict__))
    sys.exit(0)

elif albert_op == "NAME":
    sys.exit(0)

elif albert_op == "INITIALIZE":
    sys.exit(0)

elif albert_op == "FINALIZE":
    sys.exit(0)

elif albert_op == "SETUPSESSION":
    sys.exit(0)

elif albert_op == "TEARDOWNSESSION":
    sys.exit(0)

elif albert_op == "QUERY":

    albert_query = os.environ.get("ALBERT_QUERY")

    srcStr = albert_query[5:].lstrip().rstrip()


    items = []
    items.append(md5Item(srcStr))
    items.append(sha1Item(srcStr))
    items.append(sha224Item(srcStr))

    results = []
    for it in items:
        results += [json.dumps(it, default=lambda o: o.__dict__)]

    print('{"items": [' + ", ".join(results) + "]}")
    sys.exit(0)
