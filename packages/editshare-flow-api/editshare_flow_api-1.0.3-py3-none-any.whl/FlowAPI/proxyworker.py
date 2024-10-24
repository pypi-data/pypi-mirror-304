"""
FLOW Proxyworker service API
See here: https://developers.editshare.com
"""
import json

from .core import (
    PROXYWORKER_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)


class ProxyWorker(Connection):
    """Wraps the proxy worker service api"""

    def __init__(self):
        super().__init__()
        self._service_name = "proxyworker"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(ProxyWorker, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(ProxyWorker, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        """Connect to api server"""

        return Connection.connect2(self, ip_addr, PROXYWORKER_PORT, username, password)

    def createJob(self, job):
        return self.postThatReturnsObj("/jobs", job)

    def setSlotCount(self, num_slots):
        """Set the slot count"""

        job = {"slot_count": num_slots}

        reply = self.put("/config", json.dumps(job))
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def getJob(self, job_id):
        """Get a job"""

        return self.getThatReturnsObj("/jobs/" + job_id)

    def getAllJobs(self):
        """Get all jobs"""

        return self.getThatReturnsObj("/jobs")

    def deleteJob(self, job_id):
        """Delete a job"""

        reply = self.delete("/jobs/" + job_id)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("deleteProxyWorkerJob", reply)
