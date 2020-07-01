#!/bin/bash
# create user script, need root.

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



function add_user() {
    egrep "^${1}" /etc/passwd >/dev/null # 不输出任何信息到终端
    if [ $? -eq 0 ]; then
        echo "${1} 已存在"
        exit 1
    else
        useradd_cmd="sudo useradd -m ${1}"
        # echo "useradd_cmd: ${useradd_cmd}"
        eval ${useradd_cmd}
        add_passwd_cmd="sudo echo ${1}:${2} | chpasswd" 
        # echo "add_passwd_cmd: ${add_passwd_cmd}"
        eval ${add_passwd_cmd}
        
        # 修改默认终端
        row=$(grep -n "^${1}" /etc/passwd)
        row="${row/%'bin/sh'/'bin/bash'}"
        rownum="${row%%:*}"
        row="${row#*:}"
        echo ${row}
        echo ${rownum}
        echo "${rownum}c ${row}"
        sudo sed "${rownum}c ${row}" /etc/passwd
    fi
}

function to_sudoer() {
    root_row=$(grep -n "^root" /etc/sudoers)
    root_rownum=${root_row%%:*}
    rownum=$(echo "${root_rownum}+1"|bc)
    sudo sed -i "${rownum}i\\${1}	ALL=(ALL:ALL)	ALL" /etc/sudoers
}


# read -p "Enter username : " username
# read -s -p "Enter password : " password


username="test_usr212"
password="123"
# sudo userdel test_usr;rm -r /home/test_usr
add_user $username $password
# to_sudoer $username


