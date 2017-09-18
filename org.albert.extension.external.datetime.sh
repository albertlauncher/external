#!/bin/bash
# This extension shows the current date and time.
# To use this extension, type the trigger word "date" in Albert.

# The available actions copy
# - date in ISO format (e.g. 2017-09-10),
# - the full date and time (as displayed), or
# - a timestamp
# to the X clipboard. You can use Ctrl+V to paste it in other applications.
# I find the date and timestamp useful for naming files (amongst others use cases).

# Known problems:
# - If no action is executed and Albert shows up again, it still displays the
#   old time. Type "date" again to refresh.
# - Although the day name is localized by Albert's environment (environment
#   variables LANG or LC_*), the displayed date format is not.

# Why I added just these actions:
# - Date in ISO format: international standard, sorts nicely, useful for
#   filling out forms and naming files.
# - Full date and time: might be useful when you need the full date, day, time,
#   or parts thereof.
# - Timestamp with dashes: not readable without dashes; with colons in the
#   time, it would be unsuitable for filenames.
# - No "copy time only" action because I cannot think of a use case.

readonly THIS_PROGRAM=$0

executeAlbertExtension() {
  case $ALBERT_OP in
    "METADATA")
      METADATA='{
        "iid":"org.albert.extension.external/v2.0",
        "name":"Current date and time to clipboard",
        "version":"1.0",
        "author":"Jakob Schöttl",
        "dependencies":["xclip"],
        "trigger":"date"
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
    "QUERY")
      declare fullDateTime isoDate daytime timestamp
      fullDateTime=$(date +'%A, %d.%m.%Y, %H:%M Uhr')
      isoDate=$(date -I)
      #daytime=$(date +'%H:%M')
      timestamp=$(date +'%F-%H-%M-%S') # 2017-09-10-21-07-34
      RESULTS='{
        "items":[{
          "name":"'"$fullDateTime"'",
          "description":"Current date and time",
          "icon":"unknown",
          "actions":[{
            "name":"Copy '"'$isoDate'"' to clipboard",
            "command":"'"$THIS_PROGRAM"'",
            "arguments":["call-xclip", "'$isoDate'", "-r", "-selection", "clipboard"]
          },{
            "name":"Copy full date and time to clipboard",
            "command":"'"$THIS_PROGRAM"'",
            "arguments":["call-xclip", "'$fullDateTime'", "-r", "-selection", "clipboard"]
          },{
            "name":"Copy '"'$timestamp'"' to clipboard",
            "command":"'"$THIS_PROGRAM"'",
            "arguments":["call-xclip", "'$timestamp'", "-r", "-selection", "clipboard"]
          }]
        }]
        }'
      echo -n "${RESULTS}"
      exit 0
      ;;
  esac
}

# Call xclip -i with $1 as stdin and pass further args to xclip.
# That is, copy the first argument to the X clipboard.
xclipWith1stArgAsInput() {
  declare text=$1
  shift # left-shift arguments, discard $1
  xclip -i "$@" <<<"$text"
}

main() {
  declare command=$1

  if [[ $command == "call-xclip" ]]; then
    shift # discard the "call-xclip" argument
    xclipWith1stArgAsInput "$@"
  else
    executeAlbertExtension
  fi
}

main "$@"
