#! /bin/bash

git pull

filename=`date "+%Y%m%d"`.md

if [ -t 0 ]; then
    vi $filename
else
	while IFS= read -r line; do
        echo "$line" >> $filename
    done
fi

CONTEXT1=`curl -s -N http://wttr.in/\?m | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g' | head -7`
# CONTEXT1 holds the current weather and location. 
# Hat tip to http://unix.stackexchange.com/a/140255/188747 for the sed
# command to remove ansi escape codes from wttr.in output.

commit_msg="$filename updated.

$CONTEXT1"
git add $filename
git commit -m "$commit_msg" $filename && git push

