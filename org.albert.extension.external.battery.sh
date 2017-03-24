#!/bin/bash

case $ALBERT_OP in
  "METADATA")
    METADATA='{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Show Battery status",
      "version":"1.0",
      "author":"Stephan Graf",
      "dependencies":[],
      "trigger":"battery"
    }'
    echo -n "${METADATA}"
    exit 0
    ;;
  "INITIALIZE")
    exit 0
    ;;
  "FINALIZE")
    exit 0
    ;;
  "SETUPSESSION")
    exit 0
    ;;
  "TEARDOWNSESSION")
    exit 0
    ;;
  "QUERY")
    percentage=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -E "percentage:.*[0-9]+.*%" | awk '{print $2}'`
    state=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -E "state:.*" | awk '{print $2}'`
    remaining=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -E "time to empty:.*[0-9]+.*" | awk '{print $4  $5}'`
    icon=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep icon-name |awk '{print $2}' |  tr -d \'`
    echo \
'{
  "items":[{
    "name":"'${percentage}'",
    "description":"'${remaining} \(${state}\)'",
    "icon":"'${icon}'"
  }]
}'
    exit 0
    ;;
esac
