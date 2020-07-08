#!/bin/bash

script_name=".sh"
script_usage=$(cat <<EOF
$script_name [USER NAME]
EOF
)
script_function=$(cat <<EOF
This script is used to add the current or specified users as system administrator.
EOF
)
script_doc=$(cat <<EOF
-h     Display this help.
EOF
)
script_examples=$(cat <<EOF
EOF
)
state_prefix="==="
warning_prefix="***"
error_prefix="!!!"

# function get_version() {
    # curl 
# }

function get_files() {
    download_url=${1}
    hadoop_dir=${2}
    mkdir -p ~/Downloads
    wget -q -O ~/Downloads/hadoop.tar.gz ${download_url}
    tmp_dir="/tmp/$(date +%s)"
    tar -xzf ~/Downloads/hadoop.tar.gz -C ${tmp_dir}
    tmp_dir="${tmp_dir}/$(ls ${tmp_dir} | head -n 1)"
    mv ${tmp_dir} ${hadoop_dir}
}

function to_env() {
    hadoop_dir=${1}
    
}

hadoop_dir="/opt/hadoop3"
download_url="https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.2.1/hadoop-3.2.1-src.tar.gz"