#!/bin/bash

## Exit on error, var unset and pipefail
set -e -o pipefail -o nounset

send_metadata() {
    local metadata

    metadata='{
    "iid":"org.albert.extension.external/v2.0",
    "name":"Snippets Manager",
    "version":"0.2",
    "author":"turuflowers",
    "dependencies":["copyq"],
    "trigger":"s "
}'
    echo -n "${metadata}"
}

## get a row from copyq Snippets tab
copyq_get_row() {
    local copyq_row
    local count="$1"
    local n

    ## I take just the first line, in case there is a block of text
    copyq_row="$(copyq tab Snippets read text/plain "$count" | head -1 | sed -e 's/^[[:space:]]*//')"

    ## I take the name from the Note
    n="$(copyq tab Snippets read application/x-copyq-item-notes "$count" | head -1 | sed -e 's/^[[:space:]]*//')"

    # clean from non compatible json char
    printf -v clean_copyq_row "%q" "$n"
    echo -n "$clean_copyq_row"
}

## Build json object for albert query
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
        "name": "copy/paste $row",
        "command": "copyq",
        "arguments": ["tab", "Snippets", "text = read($count); copy(text); copySelection(text); paste()"]
        }
    ]
},
EOM

    echo -n "$json"
}

build_albert_query() {
    local count="$1"
    local return='{"items":['
    local json=''
    local row

    ## If the query is a number, just get that row from
    ## copyq Snippets tab
    if [[ $count =~ ^-?[0-9]+$ ]]; then
        row=$(copyq_get_row "$count")
        json=$(build_json "$count" "$row")
    else
        ## else get the last 11
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
            QUERYSTRING="${ALBERT_QUERY:3}"
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

## Call the main function
main
