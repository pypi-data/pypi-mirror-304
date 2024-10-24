"""
FLOW Sync service API
See here: https://developers.editshare.com
"""
import json

from .core import SYNC_PORT, Connection, create_gateway_instance_inner, create_instance


class Sync(Connection):
    """Wraps the sync service api"""

    # pylint: disable=consider-using-f-string

    def __init__(self):
        super().__init__()
        self._service_name = "sync"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Sync, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr="127.0.0.1"):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Sync, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        return Connection.connect2(self, ip_addr, SYNC_PORT, username, password)

    def createJob(self, job):
        reply = self.post("/sync/jobs", json.dumps(job))
        if self.lastReturnCode() != 200:
            return False
        # print "reply is"
        # print reply
        return json.loads(reply)

    def getJob(self, job_id):
        job_data = self.get("/sync/jobs/" + job_id)
        if self.lastReturnCode() != 200:
            return False
        return job_data

    def deleteJob(self, job_id):
        reply = self.delete("/sync/jobs/" + job_id)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("deleteSyncJob", reply)

    def abortJob(self, job_id):
        reply = self.put("/sync/jobs/{}/abort".format(job_id))
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("deleteSyncJob", reply)
