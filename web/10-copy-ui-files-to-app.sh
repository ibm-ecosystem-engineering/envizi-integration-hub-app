#!/usr/bin/env bash
date1=$(date '+%Y-%m-%d-%H-%M-%S')

echo "==================================================================="
echo "Copying  : Process started : " + $date1
echo "==================================================================="

## Define folder and file names
API_FOLDER_STATIC=/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/app/static
# UI_FOLDER_BUILD=./.next/
UI_FOLDER_BUILD2=./.next/static/

## Build UI files..
yarn build

## copy UI files
echo "copy UI files .........."
rm -rf ${API_FOLDER_STATIC}
mkdir -p ${API_FOLDER_STATIC}

# cp -R $UI_FOLDER_BUILD $API_FOLDER_STATIC
cp -R $UI_FOLDER_BUILD2 $API_FOLDER_STATIC
cp -R ./src/images/ $API_FOLDER_STATIC

date1=$(date '+%Y-%m-%d-%H-%M-%S')
echo "==================================================================="
echo "Copying: Process completed : " + $date1
echo "==================================================================="
