#!/bin/bash

# Use this script if you are using the DOCKER_HOST environment variable
# build and run on a remote host.

rsync_target=$(echo $DOCKER_HOST | sed -e 's/ssh:\/\/\([A-Za-z0-9\@\:\.]*\).*/\1/')
this_path=$(pwd)

rsync -Rrpv backend/code "${rsync_target}:${this_path}"
rsync -Rrpv frontend/src "${rsync_target}:${this_path}"
rsync -Rrpv webserver/ssl "${rsync_target}:${this_path}"
rsync -Rrpv etc "${rsync_target}:${this_path}"

