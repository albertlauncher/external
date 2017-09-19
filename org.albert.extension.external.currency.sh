#!/bin/bash

case $ALBERT_OP in
  "METADATA")
    METADATA='{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Currency converter",
      "version":"1.0",
      "author":"Manuel Schneider",
      "dependencies":[],
      "trigger":"exch "
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
    amount=`echo ${ALBERT_QUERY:5} | cut -d ' ' -f1`
    from=`echo ${ALBERT_QUERY:5} | cut -d ' ' -f2`
    to=`echo ${ALBERT_QUERY:5} | cut -d ' ' -f3`
    equation=`wget -qO- "https://finance.google.com/finance/converter?a=${amount}&from=${from}&to=${to}"  | sed '/res/!d;s/<[^>]*>//g'`
    [ ${#equation} -le 2 ] && exit 0
    rhs=`echo $equation | cut -d ' ' -f4-`
    echo \
'{
  "items":[{
    "name":"'${rhs}'",
    "description":"'${equation}'",
    "icon":"accessories-calculator",
    "actions":[{
      "name":"Copy to clipboard",
      "command":"sh",
      "arguments":["-c", "echo -n \"'"${rhs}"'\" | xclip -i; echo -n \"'"${rhs}"'\" | xclip -i -selection clipboard;"]
    }]
  }]
}'
    exit 0
    ;;
esac
