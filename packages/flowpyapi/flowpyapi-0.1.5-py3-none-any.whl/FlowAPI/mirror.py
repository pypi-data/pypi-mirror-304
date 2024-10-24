"""
EditShare Mirror service API
See here: https://developers.editshare.com/?urls.primaryName=EditShare%20Mirror#/
"""
from .core import Connection, create_gateway_instance_inner, create_instance


class Mirror(Connection):
    """Wraps the Mirror service api"""

    def __init__(self):
        super().__init__()
        self._service_name = "mirror"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Mirror, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Mirror, username, password, ip_addr)

    def setUseGateway(self, enable):
        """Enable using the gateway"""

        self._use_gateway = enable
        self._gateway_prefix = "/api/v1/"

    def health_check(self):
        """Simple health check"""

        return self.get("/maintenance/health")

    def get_jobs(self):
        """Get all jobs"""

        return self.getThatReturnsObj("/jobs")

    def get_job(self, job_id):
        """Get a job"""

        return self.getThatReturnsObj("/jobs/" + job_id)

    def create_job(self, job_data):
        """Create a new sync job"""

        return self.postThatReturnsObj("/jobs", job_data)

    def delete_job(self, job_id):
        """Delete a job"""

        self.delete("/jobs/" + job_id)
        return self.lastReturnCode() == 204

    def execute_job(self, job_id):
        """Execute a job"""

        return self.postThatReturnsObj("/jobs/" + job_id, None)
