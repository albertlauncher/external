#!/usr/bin/python3

import os
import re
import json

UNITS = {
# A ... Abbreviation
# T ... Type
# N ... Name (singular)
# P ... Name (plural) if this value is True, then it is assumend that the plural is built by appending a "s"
# F ... Factor in respect to SI unit
#  A   : ( T,       N,		 P,       F)
  "kg" : ("mass",  "Kilogram",	True,     1),
  "g"  : ("mass",  "Gram",      True,     10**-3),
  "lb" : ("mass",  "Pound",     True,     2.20462),
  "oz" : ("mass",  "Ounce",     True,     35.27392),
  "km" : ("length","Kilometer", True,     1000),
  "m"  : ("length","Meter",     True,     1),
  "cm" : ("length","Centimeter",True,     0.01),
  "mm" : ("length","Millimeter",True,     0.001),
  "um" : ("length","Micrometer",True,     10**-6),
  "in" : ("length","Inch",      "Inches", 39.37),
  "ft" : ("length","Foot",      True,     3.2808),
  "yd" : ("length","Yard",      True,     1.0936),
  "mi" : ("length","Mile",      True,     6.214*10**-4),
}
SI_UNIT = {
  "mass" : "kg",
  "length" : "m"
}


ALBERT_OP = os.environ['ALBERT_OP']

if ALBERT_OP == "METADATA":
  metadata = {
    "iid":"org.albert.extension.external/v2.0",
    "name":"Unit Converter",
    "version":"1.0", 
    "author":"Martin Buergmann",
    "dependencies":[],
    "trigger":"exch "
  }
  print(json.dumps(metadata))

elif ALBERT_OP == "QUERY":
  QUERY = os.environ['ALBERT_QUERY']
  pattern = re.compile("exch ([\\d\\.]+) *([^ ]+) *([^ ]+).*")
  matches = pattern.match(QUERY.lower())
  clipboard = "operation failed"
  if matches:
    try:
      amount = float(matches.group(1).lower())
      from_unit_abbr = matches.group(2).lower()
      to_unit_abbr = matches.group(3).lower()

      from_unit = False
      to_unit = False
      from_unit = UNITS[from_unit_abbr]
      to_unit = UNITS[to_unit_abbr]
      if from_unit[0] != to_unit[0]:
        result = "Nope!"
        desc = "I refuse to convert " + from_unit[1] + " to " + to_unit[1]
      else:
        from_si = SI_UNIT[from_unit[0]]
        to_si = SI_UNIT[to_unit[0]]

        si_val_from = amount if from_si == from_unit_abbr else amount / from_unit[3]
        result = si_val_from if to_si == to_unit_abbr else si_val_from * to_unit[3]
        clipboard = result
        result = "%.3e" % float(result)
        from_name = from_unit[1] if amount == 1 else from_unit[2]
        if from_name == True:
          from_name = from_unit[1] + "s"
        comp_eq1 = "is" if amount == 1 else "are"
        to_name = to_unit[1] if result == 1 else to_unit[2]
        if to_name == True:
          to_name = to_unit[1] + "s"
        desc = "%.3e %s %s %s %s" % (amount, from_name, comp_eq1, result, to_name)
    except ValueError as e:
      result = matches.group(1) + " is not a valid number"
      desc = "Expected format: \"exch <amount> <from-unit> <to-unit>\""
    except KeyError as e:
      which = "from-unit" if from_unit == False else "to-unit"
      result = which + " could not be identified as valid unit"
      desc = "Expected format: \"exch <amount> <from-unit> <to-unit>\""
    except Exception as e:
      result = str(e)
      desc = "Could not parse query"
  elif QUERY.lower() == "exch help":
    result = "Expected format:"
    desc = "exch <amount> <from-unit> <to-unit>"
  else:
    result = "..."
    desc = "This doesn't seem like a legit query"

  item = {
    "name": result,
    "description": desc, #QUERY + ": " + str(si_val_from) + from_si,
    "icon":"accessories-calculator",
    "actions":[{
      "name":"Copy to clipboard",
      "command":"sh",
      "arguments":["-c", "echo -n \"" + str(clipboard) + "'\" | xclip -i; echo -n \"" + str(clipboard) + "\" | xclip -i -selection clipboard;"]
    }]
  }
  print("{\"items\":[" + json.dumps(item) + "]}")


