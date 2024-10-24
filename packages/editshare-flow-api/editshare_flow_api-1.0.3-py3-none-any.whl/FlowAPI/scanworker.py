"""
FLOW Scan worker service API
See here: https://developers.editshare.com
"""

from .core import (
    SCANWORKER_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)


class ScanWorker(Connection):
    """Wraps the scan worker service api"""

    def __init__(self):
        super().__init__()
        self._service_name = "scanworker"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(ScanWorker, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(ScanWorker, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        """Connect to service server"""

        return Connection.connect2(self, ip_addr, SCANWORKER_PORT, username, password)

    def create_job(self, job):
        return self.postThatReturnsObj("/scanworkers/jobs", job)

    def get_config(self):
        return self.getThatReturnsObj("/scanworkers/config")

    def put_config(self, config):
        return self.put("/scanworkers/config", config)

    def get_status(self):
        return self.getThatReturnsObj("/scanworkers/status")

    def get_job(self, job_id):
        return self.getThatReturnsObj("/scanworkers/jobs/" + job_id)

    def get_mediaspace_scan(self, job_id):
        return self.getThatReturnsObj("/scanworkers/mediaspace/" + job_id)

    def get_asset_scan(self, job_id):
        return self.getThatReturnsObj("/scanworkers/asset/" + job_id)

    def stop_job(self, job_id):
        return self.put("/scanworkers/{}/stop".format(job_id))
