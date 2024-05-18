import wmi

def get_volume_serial_number(drive_letter):
    """
    获取指定分区的卷序列号。

    参数：
        drive_letter (str): 要查询的分区盘符，例如 "C:"。

    返回：
        str: 如果成功获取卷序列号，则返回该卷的序列号；如果失败，则返回 None。
    """
    try:
        c = wmi.WMI()
        for logical_disk in c.Win32_LogicalDisk():
            if logical_disk.Caption == drive_letter:
                return logical_disk.VolumeSerialNumber
    except Exception as e:
        print(f"Error occurred while retrieving serial number: {e}")
    return None

def get_drive_letter(serial_number):
    """
    根据卷序列号查找相应的分区盘符。

    参数：
        serial_number (str): 要查找的卷序列号。

    返回：
        str: 如果找到匹配的卷序列号，则返回相应的分区盘符；如果未找到，则返回 None。
    """
    try:
        c = wmi.WMI()
        for logical_disk in c.Win32_LogicalDisk():
            if logical_disk.VolumeSerialNumber.upper() == serial_number.upper():
                return logical_disk.Caption
    except Exception as e:
        print(f"Error occurred while retrieving drive letter: {e}")
    return None
