#! /bin/bash

git pull

filename=`date "+%Y%m%d"`.md

if [ ! -e $filename ]; then
	echo '```'>> $filename && \
	date '+%A, %B %d %Y' >> $filename && \
	curl -s -N http://wttr.in/\?m | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g' | head -7 >> $filename &&\
	echo '```'>> $filename && \
	echo  >> $filename
fi

if [ -t 0 ]; then
    vi $filename
else
	while IFS= read -r line; do
        echo "$line" >> $filename
    done
fi


commit_msg="$filename updated."
CONTEXT_WEATHER=`curl -s -N http://wttr.in/\?m | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g' | head -7`
git add $filename
git commit -m "$commit_msg
$CONTEXT_WEATHER
" $filename && git push


# the curl wttr.in command outputs holds the current weather and 
# current location. Hat tip to http://unix.stackexchange.com/a/140255/188747 
# for the sed command to remove ansi escape codes from wttr.in output.
