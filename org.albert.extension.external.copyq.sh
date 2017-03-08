#!/bin/bash

set -e -o pipefail -o nounset

copyq_get_row(){
    local copyq_row="$(copyq read $1 | head -1 | sed -e 's/^[[:space:]]*//')"

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
    "id": "h$count",
    "name": "$row",
    "icon": "/usr/share/icons/hicolor/scalable/apps/copyq-normal.svg",
    "description": "$count",
    "actions": [{
        "name": "$row",
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

    if [[ $count =~ ^-?[0-9]+$ ]]; then
        local row=$(copyq_get_row "$count")
        json=$(build_json "$count" "$row")
    else
        for count in {0..10}; do
            local row=$(copyq_get_row "$count")
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
            STDOUT='{
                "iid":"org.albert.extension.external/v2.0",
                "name":"Clipboard Manager",
                "version":"1.1",
                "author":"BarbUk",
                "dependencies":["copyq"],
                "trigger":"h"
            }'
            echo -n "${STDOUT}"
            exit 0
        ;;

        "QUERY")
            ALBERT_QUERY=${ALBERT_QUERY:-}
            QUERYSTRING="${ALBERT_QUERY:2}"
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
