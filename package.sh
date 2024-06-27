#!/usr/bin/env bash
set -xe
version=$(jq -r ".app_version" ctis.json)
mkdir -p build
timestamp=$(date +%s)
output="build/ctis-$version-${timestamp}.tgz"
echo "Output: $output"
name_of_this_dir=$(basename "$(pwd)")
tar --exclude=".*" --exclude="build" -C ../ -czvf "$output" "$name_of_this_dir"
