"""
FLOW Daemon service API
See here: https://developers.editshare.com
"""
import json

from .core import DAEMON_PORT, Connection


class Daemon(Connection):
    """Wraps the Daemon service api"""

    # Connect to server
    def connect(self, ip, username, password):
        return Connection.connect2(self, ip, DAEMON_PORT, username, password)

    def mount(self, mediaSpaceName, localMountPoint, taskName="Python API"):
        data = {
            "mediaspace_name": mediaSpaceName,
            "mount_directory": localMountPoint,
            "task_name": taskName,
        }
        reply = self.put("/mount/mount", json.dumps(data))
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("mount", reply)

    def unmount(self, mediaSpaceName, localMountPoint, taskName="Python API"):
        data = {
            "mediaspace_name": mediaSpaceName,
            "mount_directory": localMountPoint,
            "task_name": taskName,
        }
        reply = self.put("/mount/unmount", json.dumps(data))
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("mount", reply)

    def createISISSetupJob(self):
        return self.postThatReturnsObj("/configuration/setup/isis", "")

    def getConfigurationJob(self, jobID):
        rv = self.get("/configuration/setup/" + jobID)
        return rv

    def controlService(self, serviceName, action):
        reply = self.put("/services/" + serviceName + "/" + action)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("controlService", reply)
