#!/usr/bin/env bash
set -xe
version=$(jq -r ".app_version" ctis.json)
bumped_version=$(echo "$version" | awk -F. '/[0-9]+\./{$NF++;print}' OFS=.)
echo "Version bump: $version -> $bumped_version"
jq ".app_version = \"$bumped_version\"" ctis.json > ctis.json.tmp
mv ctis.json.tmp ctis.json

mkdir -p build
timestamp=$(date +%s)
output="build/ctis-$bumped_version-${timestamp}.tgz"
echo "Output: $output"
name_of_this_dir=$(basename "$(pwd)")
tar --exclude=".*" --exclude="build" -C ../ -czvf "$output" "$name_of_this_dir"
