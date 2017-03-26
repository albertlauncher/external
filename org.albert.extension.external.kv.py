#!/usr/bin/env python
import json
import os
import sqlite3
import sys

class Object(object):
    pass

# the path place db file for kv plugin
dbFile = "{0}{1}".format(os.path.split(os.path.realpath(__file__))[0], "/../kv.db")
meFile = sys.argv[0]

def item(id, name, desc, icon):
    item = Object()
    item.id = id
    item.name = name
    item.description = desc
    item.icon = icon
    item.actions = []

    return item

def action(name, command, arguments):
    action = Object()
    action.name = name
    action.command = command
    action.arguments = arguments
    return action


def createTalbe():
    conn.execute("""
        CREATE TABLE  IF NOT EXISTS kv
        (
            id     INTEGER PRIMARY KEY    AUTOINCREMENT,
            key                TEXT   NOT NULL,
            value              TEXT   NOT NULL
        );
    """)


def set(key, value):
    conn.execute("INSERT INTO kv(`key`,`value`) VALUES('{0}','{1}')".format(key, value))
    conn.commit()
    return


def get(key):
    cursor = conn.execute("SELECT id, `key`, `value` FROM kv WHERE `key` LIKE '%{0}%'".format(key))
    kvs = []
    for row in cursor:
        kv = Object()
        kv.key = row[1]
        kv.value = row[2]
        kvs.append(kv)
    cursor.close()
    return kvs


def delete(key):
    cursor = conn.execute("DELETE FROM kv WHERE `key` = '{0}'".format(key))
    conn.commit()
    cursor.close()
    return


# debug
def filelog(str):
    # f=open("{0}/../testplugin.log".format(os.path.split(os.path.realpath(__file__))[0]),"a")
    # f.writelines(str)
    # f.writelines("\n")
    # f.close()
    return


albert_op = os.environ.get("ALBERT_OP")
mode = os.environ.get("MODE")

if albert_op == "METADATA":
    metadata = Object()
    metadata.iid = "org.albert.extension.external/v2.0"
    metadata.name = "kv"
    metadata.version = "1.0"
    metadata.author = "glight2000"
    metadata.dependencies = []
    metadata.trigger = "kv"
    print(json.dumps(metadata, default=lambda o: o.__dict__))

elif albert_op == "NAME":
    sys.exit(0)

elif albert_op == "INITIALIZE":
    conn = sqlite3.connect(dbFile)
    createTalbe()
    conn.close()
    sys.exit(0)

elif albert_op == "FINALIZE":
    sys.exit(0)

elif albert_op == "SETUPSESSION":
    sys.exit(0)

elif albert_op == "TEARDOWNSESSION":
    sys.exit(0)

elif albert_op == "QUERY":
    albert_query = os.environ.get("ALBERT_QUERY").lstrip().rstrip()
    query = albert_query.split()

    items = []

    if len(query) < 2:
        items.append(item("kv", "wait intent 'set' or 'get'  {0}".format(query), "", ""))
    else:
        conn = sqlite3.connect(dbFile)
        intent = query[1].lstrip().rstrip()
        if intent == "set":
            key = ""
            value = ""
            if len(query) == 3:
                key = query[2].lstrip().rstrip()
            elif len(query) >= 4:
                key = query[2].lstrip().rstrip()
                value = query[3].lstrip().rstrip()

            i = item("kv-set", "set", "key:{0} value:{1}".format(key, value), "")
            i.actions.append(action("copy value to clipboard", meFile,  ["dset", key, value]))
            items.append(i)
            filelog("{0} {1}".format(i.actions[0].command,i.actions[0].arguments))
        elif intent == "get":
            key = ""
            if len(query) == 3:
                key = query[2].lstrip().rstrip()
                kvs = get(key)
                if len(kvs) == 0:
                    items.append(item("kv-get", "no record found", "key:{0}".format(key), ""))
                for kv in kvs:
                    i = item("kv-get", kv.key, kv.value, "")
                    i.actions.append(action("copy value to clipboard","sh",  ["-c", 'echo -n "{0}" | xclip -i -selection clipboard;'.format(kv.value)]))
                    items.append(i)
            else:
                items.append(item("kv-get", "get", "key:{0}".format(key), ""))
        elif intent == "del":
            key = ""
            if len(query) == 3:
                key = query[2].lstrip().rstrip()
                kvs = get(key)
                if len(kvs) == 0:
                    items.append(item("kv-get", "no record found", "key:{0}".format(key), ""))
                for kv in kvs:
                    i = item("kv-del", kv.key, kv.value, "")
                    i.actions.append(action("copy value to clipboard", meFile,  ["ddel", kv.key]))
                    items.append(i)
            else:
                items.append(item("kv-get", "get", "key:{0}".format(key), ""))
        else:
            items.append(item("kv", "wait intent 'set' or 'get'  {0}".format(query), "", ""))

        conn.close()

    results = []
    for it in items:
        results += [json.dumps(it, default=lambda o: o.__dict__)]

    print('{"items": [' + ", ".join(results) + '],"variables":{"va":"aaa","vb":"bbb"}}')
    sys.exit(0)

else:
    filelog("no albert_op indicated")

    intent = ""
    if len(sys.argv) >= 2:
        intent = sys.argv[1]
    else:
        filelog("Intent error : none")
        sys.exit(0)

    filelog(intent)

    conn = sqlite3.connect(dbFile)
    if intent == "dset":
        if len(sys.argv) >= 4:
            key = sys.argv[2].lstrip().rstrip()
            value = sys.argv[3].lstrip().rstrip()
            delete(key)
            set(key, value)
            filelog("set {0} {1} ok".format(key,value))
        else:
            filelog("Set error : not enough arguments")
    elif intent == "dget":
        if len(sys.argv) >= 3:
            key = sys.argv[2].lstrip().rstrip()
            filelog("get {0} : {1}".format(key, get(key)))
        else:
            filelog("Get error : not enough arguments")
    elif intent == "ddel":
        if len(sys.argv) >= 3:
            key = sys.argv[2].lstrip().rstrip()
            delete(key)
            filelog("delete {0} done".format(key))
        else:
            filelog("Get error : not enough arguments")
    else:
        filelog("Intent error : {0}".intent)
    conn.close()

    sys.exit(0)
