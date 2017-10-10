#!/bin/bash

## Exit on error, var unset and pipefail
set -e -o pipefail -o nounset

send_metadata() {
    local metadata

    metadata='{
        "iid":"org.albert.extension.external/v3.0",
        "name":"CopyQ",
        "version":"1.5",
        "author":"BarbUk",
        "dependencies":["copyq"],
        "trigger":"cq ",
        "description": "Access to the CopyQ clipboard manager.",
        "usage_example": "cq <search string>"
    }'
    echo -n "${metadata}"
}

## search a string in copyq stack
copyq_search_row() {
    local string="$1"
    local script="var match = '$string';
var i =0;
while ( i < size() ) {
    if ( str(read(i)).indexOf(match) !== -1 ) {
        print(i + ' ');
    }
    ++i;
}"
    echo "$script" | copyq eval -
}

## get a row from copyq history stack
copyq_get_row() {
    local copyq_row
    local count="$1"

    ## I take just the first line, in case there is a block of text
    copyq_row="$(copyq read text/plain "$count" | tr -d '\n' | sed -e 's/^[[:space:]]*//')"

    # clean from non compatible json char
    printf -v clean_copyq_row "%q" "$copyq_row"
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
    "icon": "copyq-normal",
    "actions": [
        {
            "name": "paste directly",
            "command": "copyq",
            "arguments": ["select($count); sleep(100); paste()"]
        },
        {
            "name": "copy to clipboard",
            "command": "copyq",
            "arguments": ["select", "$count"]
        }
    ]
},
EOM

    echo -n "$json"
}

build_albert_query() {
    local query="$1"
    local return='{"items":['
    local json=''
    local row

    ## If there is a query, search for it
    if [ -n "$query" ]; then
        ids=$(copyq_search_row "$query")
    else # else get the last 20 items
        ids=$(seq 0 19)
    fi
    for id in $ids; do
        row=$(copyq_get_row "$id")
        if [[ "$row" == "''" ]]; then
            continue
        fi
        new=$(build_json "$id" "$row")
        json="$json$new"
    done

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
            build_albert_query "$ALBERT_QUERY"
            exit 0
        ;;
        "INITIALIZE")
            if ! which copyq >/dev/null 2>&1; then
                echo "You need to install copyq" >&2
                exit 1
            fi

            exit 0
        ;;
        "FINALIZE")
            exit 0
        ;;
    esac
}

## Call the main function
main
