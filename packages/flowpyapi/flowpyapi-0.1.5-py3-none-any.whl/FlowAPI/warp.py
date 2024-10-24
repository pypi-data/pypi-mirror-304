"""
EditShare Warp service API
See here: https://developers.editshare.com/?urls.primaryName=EditShare%20Warp
"""
from .core import Connection, create_gateway_instance_inner, create_instance


class Warp(Connection):
    """Wraps the Warp service api"""

    def __init__(self):
        super().__init__()
        self._service_name = "warp"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Warp, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Warp, username, password, ip_addr)

    def setUseGateway(self, enable):
        """Enable using the gateway"""

        self._use_gateway = enable
        self._gateway_prefix = "/api/v1/"

    def health_check(self):
        """Simple health check"""

        return self.get("/maintenance/health")

    def get_transfer(self, transfer_id):
        """Get a transfer"""

        return self.getThatReturnsObj("/transfers/" + transfer_id)

    def create_job(self, job_data):
        """Create a new transfer job

        On success 201 code is returned
        :returns: Dict of the warp job. id key is "id"
        """

        return self.postThatReturnsObj("/transfers", job_data)

    def delete_job(self, transfer_id):
        """Delete a transfer"""

        self.delete("/transfers/" + transfer_id)
        return self.lastReturnCode() == 204
