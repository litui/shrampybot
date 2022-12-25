#!/bin/bash

# Use this script if you are using the DOCKER_HOST environment variable
# build and run on a remote host.

rsync_target=$(echo $DOCKER_HOST | sed -e 's/ssh:\/\/\([A-Za-z0-9\@\:\.]*\).*/\1/')
this_path=$(pwd)

rsync -uRrpv backend/code "${rsync_target}:${this_path}"
rsync -uRrpv frontend/src "${rsync_target}:${this_path}"
rsync -uRrpv webserver/ssl "${rsync_target}:${this_path}"
rsync -uRrpv etc "${rsync_target}:${this_path}"

