#!/bin/bash
# Call xclip -i with $1 as stdin and pass further args to xclip.
# That is, copy the first argument to the X clipboard.

declare text=$1
shift # left-shift arguments, discard $1
xclip -i "$@" <<<"$text"
