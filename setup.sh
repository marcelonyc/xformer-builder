#! /bin/bash

log_error () {
    echo -e "[`date`]\033[31mERROR: $1\033[0m"
}

log_task () {
    echo -e "[`date`]\033[32mTASK: $1\033[0m"
}

log_task "Checking dependencies"
command -v git > /dev/null
if [ $? -ne 0 ]; then
    log_error "git is not installed"
    exit 1
fi

command -v python > /dev/null
if [ $? -ne 0 ]; then
    log_error "Python is not installed"
    exit 1
fi

PROJECT_DIR=$(pwd)
ASSETS_DIR=${PROJECT_DIR}/controlplane/src/assets
mkdir -p ${ASSETS_DIR}/src-noconflict/snippets
_WORK_DIR=$(pwd)/$$
mkdir -p $_WORK_DIR
if [ $? -ne 0 ]; then
    log_error "Failed to create work directory"
    exit 1
fi
cd $_WORK_DIR

log_task "Downloading ACE editor"
git clone -b v1.5.0 https://github.com/ajaxorg/ace-builds.git 
if [ $? -ne 0 ]; then
    log_error "Failed to download ACE editor"
    exit 1
fi

log_task "Copying ACE editor files"
cp ace-builds/src-noconflict/* ${ASSETS_DIR}/src-noconflict/.  > /dev/null 2>&1
if [ $? -ne 0 ]; then
    log_error "Failed to copy ACE editor files"
    exit 1
fi
cp ace-builds/src-noconflict/snippets/python.js ${ASSETS_DIR}/src-noconflict/snippets/. > /dev/null 2>&1
if [ $? -ne 0 ]; then
    log_error "Failed to copy ACE Python editor files"
    exit 1
fi
log_task "Cleaning up"
cd ${PROJECT_DIR}
rm -fr $_WORK_DIR

log_task "Installing Python dependencies"
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    log_error "Failed to install Python dependencies"
    exit 1
fi


log_task "Vault Configuration"
log_task "Data Provider Configuration"
log_task "Generate Config Yaml"

log_task "Setup complete"

