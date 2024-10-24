"""
EditShare WatchFolder service API
See here: https://developers.editshare.com
"""
import json

from .core import Connection, create_gateway_instance_inner


class WatchFolder(Connection):
    """Wraps the proxy worker service api"""

    def __init__(self):
        super().__init__()
        self._service_name = "watchfolder"

    @staticmethod
    def create_gateway_instance(credentials, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(
            WatchFolder, credentials[0], credentials[1], ip_addr
        )

    def create_job(self, job):
        """Create a new watchfolder job

        :returns: The new job dict
        """

        return self.postThatReturnsObj("/jobs", job)

    def get_job(self, job_id):
        """Get a job

        :returns: A dict of the job
        """

        return self.getThatReturnsObj("/jobs/" + job_id)

    def get_all_jobs(self):
        """Get all jobs

        :returns: A list of job dicts
        """

        return self.getThatReturnsObj("/jobs")

    def find_job(self, job_name):
        """Find a job with the given name

        :returns: The job dict
        """

        all_jobs = self.get_all_jobs()
        for existing_job in all_jobs:
            if existing_job["name"] == job_name:
                return existing_job
        return {}

    def delete_job(self, job_id):
        """Delete a job

        :returns: boolean
        """

        reply = self.delete("/jobs/" + job_id)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("deleteWatchFolderJob", reply)

    def get_changes(self, job_id, discard=False):
        """Get the changes for a job and optionally discard them

        :returns: A changes dict - see docs
        """

        changes = self.getThatReturnsObj("/jobs/" + job_id + "/changes")
        if changes and discard:
            self.discard_changes(job_id, changes)
        return changes

    def discard_changes(self, job_id, changes):
        """Discard changes

        :returns: The number of changes discarded as an int
        """

        if not changes:
            return 0

        id_list = []
        start_id = -1
        end_id = -1
        for change in changes:
            change_id = change["file-change-id"]
            id_list.append(change_id)
            if start_id < 0:
                start_id = end_id = change_id
            elif change_id == end_id + 1:
                end_id = change_id
            else:
                end_id = -1

        if start_id > 0 and end_id == start_id + 1:
            discard_data = {"ranges": [{"first": start_id, "last": end_id}]}
        else:
            discard_data = {"list": id_list}
        # print(discard_data)
        reply = self.put("/jobs/" + job_id + "/discard", json.dumps(discard_data))
        if self.lastReturnCode() != 200:
            return 0
        return int(reply)
