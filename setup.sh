#! /bin/bash

command -v git > /dev/null
if [ $? -ne 0 ]; then
    echo "git is not installed"
    exit 1
fi

command -v git > /dev/null
if [ $? -ne 0 ]; then
    echo "Python is not installed"
    exit 1
fi

PROJECT_DIR=$(pwd)
ASSETS_DIR=${PROJECT_DIR}/coding/assets
mkdir -p ${ASSETS_DIR}/src-noconflict/snippets
_WORK_DIR=$(pwd)/$$
mkdir -p $_WORK_DIR
cd $_WORK_DIR

git clone -b v1.5.0 https://github.com/ajaxorg/ace-builds.git 
cp ace-builds/src-noconflict/* ${ASSETS_DIR}/src-noconflict/.
cp ace-builds/src-noconflict/snippets/python.js ${ASSETS_DIR}/src-noconflict/snippets/.

cd ${PROJECT_DIR}
rm -fr $_WORK_DIR

pip install -r requirements.txt

