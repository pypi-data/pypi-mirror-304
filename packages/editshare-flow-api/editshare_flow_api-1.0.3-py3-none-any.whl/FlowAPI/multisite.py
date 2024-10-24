"""
FlowAPI / EditShare Multisite
Wraps this API: https://developers.editshare.com/?urls.primaryName=EditShare%20Multisite
"""

from .core import Connection, create_gateway_instance_inner, create_instance


class Multisite(Connection):
    """Wraps the storage multisite service api"""

    def __init__(self):
        super().__init__()
        self._service_name = "multisite"

    @staticmethod
    def create_instance(ip, username, password):
        """Create and connect directly to service server"""

        return create_instance(Multisite, ip, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Multisite, username, password, ip_addr)

    def connect(self, ip, username, password):
        """Connect to service server"""

        self.setUseGateway(True)
        self._gateway_prefix = "/api/v1/"
        return Connection.connect2(self, ip, 0, username, password)

    def get_sites(self):
        """Get the list of sites"""

        return self.getThatReturnsObj("/sites")

    def add_site(self, site_data):
        """Add a new site"""

        return self.postThatReturnsObj("/sites", site_data)

    def update_site(self, site_uuid, site_data):
        """Update an existing site"""

        return self.patch_to_bool("update_site", "/sites/" + str(site_uuid), site_data)
