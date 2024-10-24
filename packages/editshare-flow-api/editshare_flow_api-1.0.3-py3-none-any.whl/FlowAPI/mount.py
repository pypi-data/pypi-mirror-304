"""Functions for mounting EFS or SMB from within Linux and Windows

Some EFS command line items
: ['EditShare File System.exe', '-H', '192.168.97.82', '-S', '/Unmanaged/mfh-home_1/Content', '--volume-name=mfh-home_1',
'--log-file=C:\\Users\\editshare\\AppData\\Local\\EditShare\\native_client_log_mfh-home_1',
'--tls=yes', '--tls-ca-dir=C:/Program Files (x86)/EditShare/EditShare Connect/es_connect/resources/certs/',
'--minimal-directory-permissions=2770', '--minimal-file-permissions=660', '--enable-distributed-file-range-locks=yes',
'--disable-sharing-restrictions=no', '-U', 'mhallin', '--limitGroup=/mhallin:192.168.97.248', 'Y:']

"EditShare File System.exe" -H 192.168.97.82 --user=mhallin --password=xxxx --subfolder=/Unmanaged/mfh-home_1/Content --volume-name=mfh-home_1 --minimal-directory-permissions=2770 Y:
efs-client -H 192.168.97.82 --user=mhallin --password=xxx --subfolder=/Unmanaged/mfh-home_1/Content --volume-name=mfh-home_1 /home/editshare/testmount

from fstab

mount-efs-client /efs/flow fuse host=es-scotland,user=_flow_proxy_519e2334d2d64657,password-file=/etc/efs/flow_password,subfolder=flow,tls=yes,tls-ca-dir=/etc/editshare/ssl/certs,fake-uid=494,fake-gid=494,_netdev 0 0
efs-mount /efs/efs_1 fuse host=es-scotland,user=_efs_519e2334d2d64657a93ffeb8f2077130,password-file=/etc/efs/client_password,_netdev,metawatch=yes,metawatch-show-path=yes,metawatch-get-mine=yes 0 0

"""
import logging
import os
import platform
import shlex
import subprocess
import time


def _smb_mount_windows(letter, host, user, password, ms_name, mount):
    if mount:
        cmd = 'net use {}: "\\\\{}\\{}_1" /user:{} {}'.format(
            letter, host, ms_name, user, password
        )
    else:
        cmd = "net use {}: /del".format(letter)

    logging.debug("_smb_mount_windows: %s", cmd)

    result = subprocess.call(cmd, shell=True)

    if result != 0:
        logging.warning("Failed to (un)mount drive")
        return False

    return True


def _efs_mount_options(mount_point, host, user, password, ms_name, ms_type):
    """Return EFS mount options."""
    ms_type_lower = ms_type.lower()
    ms_folder = "no folder"

    if ms_type_lower == "unmanaged":
        ms_folder = "Unmanaged"
    elif ms_type_lower == "managed":
        ms_folder = "Managed"
    elif ms_type_lower == "avidstyle":
        ms_folder = "AvidStyle"
    elif ms_type_lower == "avidmxf":
        ms_folder = "AvidMXF"

    extra_options = [
        "--minimal-directory-permissions=2770",
        "--minimal-file-permissions=660",
        "--enable-distributed-file-range-locks=yes",
    ]
    cmds = []
    cmds.append("-H {}".format(host))
    cmds.append("--user={}".format(user))
    cmds.append("--password={}".format(password))
    cmds.append("--subfolder=/{}/{}_1/Content".format(ms_folder, ms_name))
    cmds.append("--volume-name={}_1".format(ms_name))
    cmds += extra_options
    cmds.append(mount_point)

    # print(cmds)
    cmd = " ".join(cmds)
    return cmd


def _efs_mount_linux(mount_point, host, user, password, ms_name, ms_type, mount):
    # if not os.path.isdir(mount_point):
    # os.makedirs(mount_point)

    if mount:
        bin_path = "efs-client"

        opts = _efs_mount_options(mount_point, host, user, password, ms_name, ms_type)

        cmd = "sudo {} {}".format(bin_path, opts)

    else:
        cmd = "sudo umount {}".format(mount_point)

    logging.debug("_efs_mount_linux: %s", cmd)
    result = subprocess.call(cmd, shell=True)

    if result != 0:
        logging.warning("_efs_mount_linux: Failed to (un)mount drive")
        return False

    return True


def _efs_mount_windows(letter, host, user, password, ms_name, ms_type, mount):
    if mount:
        bin_path = '"C:\\Program Files (x86)\\EditShare\\EditShare Connect\\EditShare File System.exe"'

        opts = _efs_mount_options(
            "{}:".format(letter), host, user, password, ms_name, ms_type
        )

        cmd = "{} {}".format(bin_path, opts)

    else:
        cmd = "net use {}: /del".format(letter)

    logging.debug("_efs_mount_windows: %s", cmd)

    if mount:
        result = 0
        process = subprocess.Popen(shlex.split(cmd))
        time.sleep(1)
        process.poll()
        if process.returncode is not None:
            print(process.returncode)
            result = process.returncode
    else:
        result = subprocess.call(cmd, shell=True)

    if result != 0:
        logging.error("_efs_mount_windows: Failed to (un)mount drive. %s", cmd)
        return False

    return True


def _smb_mount_linux(mount_point, host, user, password, ms_name, mount):
    if not os.path.isdir(mount_point):
        os.makedirs(mount_point)

    if mount:
        cmd = "sudo mount -t cifs -o user={},pass={},rw,noperm,iocharset=utf8,noserverino //{}/{}_1 {}".format(
            user, password, host, ms_name, mount_point
        )
    else:
        cmd = "sudo umount {}".format(mount_point)

    logging.debug("_smb_mount_linux: %s", cmd)
    result = subprocess.call(cmd, shell=True)

    if result != 0:
        logging.error("_smb_mount_linux: Failed to (un)mount drive. %s", cmd)
        return False

    return True


def efs_mount(host, user, password, ms_name, ms_type, mount_point):
    """EFS mount."""
    if platform.system().lower() == "windows":
        result = _efs_mount_windows(
            mount_point[0], host, user, password, ms_name, ms_type, True
        )
    else:
        result = _efs_mount_linux(
            mount_point, host, user, password, ms_name, ms_type, True
        )

    return result


def efs_unmount(mount_point):
    """Unmount EFS mount."""
    if platform.system().lower() == "windows":
        result = _efs_mount_windows(mount_point[0], None, None, None, None, None, False)
    else:
        result = _efs_mount_linux(mount_point, None, None, None, None, None, False)

    return result


def smb_mount(host, user, password, ms_name, ms_type, mount_point):
    """SMB mount."""
    if platform.system().lower() == "windows":
        result = _smb_mount_windows(mount_point[0], host, user, password, ms_name, True)
    else:
        result = _smb_mount_linux(mount_point, host, user, password, ms_name, True)

    return result


def smb_unmount(mount_point):
    """Unmount SMB mount."""
    if platform.system().lower() == "windows":
        result = _smb_mount_windows(mount_point[0], None, None, None, None, False)
    else:
        result = _smb_mount_linux(mount_point, None, None, None, None, False)

    return result


def get_mount_dir(app_name):
    """Return local mount dir"""

    if platform.system() == "Windows":
        drives = [
            "E",
            "F",
            "G",
            "H",
            "J",
            "K",
            "L",
            "M",
            "N",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
        ]
        for drive in drives:
            to_try = "{}:\\".format(drive)
            if not os.path.isdir(to_try):
                return to_try

        return None

    return "/mnt/flow/{}".format(app_name)


def is_mounted(mount_point):
    """Is the mount point mounted?."""
    if platform.system().lower() == "windows":
        return os.path.exists(mount_point)

    with open("/proc/mounts", "r") as file_handle:
        content = file_handle.read()

    # logging.debug( content )

    if mount_point in content:
        return True

    return False


def main():
    logging.basicConfig(level=logging.DEBUG)

    efs_mount("192.168.97.82", "mhallin", "matt0479", "mfh-home", "unmanaged", "Y:")
    # efs_unmount( "Y:")


if __name__ == "__main__":
    main()
