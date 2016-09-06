#! /bin/bash

git pull

filename=`date "+%Y%m%d"`.md
echo $filename
vi $filename
commit_msg="$filename updated"
git add $filename
git commit -m "$commit_msg" $filename && git push

