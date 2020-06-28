#!/bin/bash
#代码来自https://www.cnblogs.com/quantumman/p/4581846.html

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
