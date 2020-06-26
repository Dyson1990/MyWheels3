#!/bin/bash
hive_path=$(whereis hive)
#echo $hive_dir
eval nohup $hive_path --service hiveserver2 > ~/log/hive.log &
