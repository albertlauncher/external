#!/bin/bash

set -e -o pipefail -o nounset

send_metadata() {
    local metadata

    metadata='{
    "iid":"org.albert.extension.external/v2.0",
    "name":"Clipboard Manager",
    "version":"1.2",
    "author":"BarbUk",
    "dependencies":["copyq"],
    "trigger":"hist"
}'
    echo -n "${metadata}"
}

copyq_get_row() {
    local copyq_row
    local count="$1"
    copyq_row="$(copyq read text/plain "$count" | head -1 | sed -e 's/^[[:space:]]*//')"
    # clean from non compatible json char
    printf -v clean_copyq_row "%q" "$copyq_row"
    echo -n "$clean_copyq_row"
}

build_json() {
    local count="$1"
    shift 1
    local row="$*"

    read -r -d '' json << EOM
{
    "name": "$row",
    "icon": "/usr/share/icons/hicolor/scalable/apps/copyq-normal.svg",
    "description": "$count",
    "actions": [{
        "name": "copy $row to clipboard",
        "command": "copyq",
        "arguments": ["select", "$count"]
    }]
},
EOM

    echo -n "$json"
}

build_albert_query() {
    local count="$1"
    local return='{"items":['
    local json=''
    local row

    if [[ $count =~ ^-?[0-9]+$ ]]; then
        row=$(copyq_get_row "$count")
        json=$(build_json "$count" "$row")
    else
        for count in {0..10}; do
            row=$(copyq_get_row "$count")
            if [[ "$row" == "''" ]]; then
                continue
            fi
            new=$(build_json "$count" "$row")

            json="$json$new"
        done
    fi
    # remove last comma
    json=${json::-1}

    return="$return$json]}"
    echo -n "$return"
}

main() {
    case $ALBERT_OP in
        "METADATA")
            send_metadata
            exit 0
        ;;

        "QUERY")
            ALBERT_QUERY=${ALBERT_QUERY:-}
            QUERYSTRING="${ALBERT_QUERY:5}"
            build_albert_query "$QUERYSTRING"
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
    esac
}
main
