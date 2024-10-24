"""
FlowAPI / FLOW Scan service API
See here: https://developers.editshare.com/?urls.primaryName=EditShare%20FLOW%20Scan
"""
import json
import logging
import time

from .core import SCAN_PORT, Connection, create_gateway_instance_inner, create_instance


class Scan(Connection):
    """Wraps the scan service api"""

    # pylint: disable=too-many-public-methods,consider-using-f-string

    def __init__(self):
        super().__init__()
        self._service_name = "scan"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Scan, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr="127.0.0.1"):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Scan, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        """Connect to service server"""

        return Connection.connect2(self, ip_addr, SCAN_PORT, username, password)

    def get_jobs(self, start=0, count=100):
        """Get all scan jobs
        note that start/count params are for future use
        """

        return self.getThatReturnsObj("/scan/jobs")

    def get_job(self, job_uuid):
        """Get a specific job"""

        return self.getThatReturnsObj("/scan/jobs/{}".format(job_uuid))

    def get_job_progress(self, job_uuid):
        """Get job progress"""

        return self.getThatReturnsObj("/scan/jobs/{}/progress".format(job_uuid))

    def get_job_results(self, job_uuid):
        """Get job results"""

        return self.getThatReturnsObj("/scan/jobs/{}/results".format(job_uuid))

    def scanAsset(self, job):
        """Start a single asset scan"""

        reply = self.post("/scan/asset", json.dumps(job))
        # print reply
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def proxyManagmentScan(self):
        """Start a proxy management scan"""

        reply = self.post("/scan/proxymanagement", "")
        # print reply
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def scanMediaspace(self, mediaspace, create_proxies=True, scan_type="normal"):
        """Scans a media space using default settings, takes media space name as only argument
        Does not check to see if media space exists or not, just tries to run the scan
        """

        return self.scanMediaspaceInner(
            mediaspace, "", False, create_proxies, scan_type
        )

    def scanMediaspaceInner(
        self, mediaspace, directory, recursive, create_proxies, scan_type
    ):
        # pylint:disable=too-many-arguments
        """Start a mediaspace scan"""

        job = {
            "auto-delete": "false",
            "create-proxies": create_proxies,
            "scan-type": scan_type,
            "mediaspaces": [mediaspace],
            "recursive": recursive,
        }

        if directory:
            job["start_path"] = directory

        reply = self.post("/scan/mediaspace", json.dumps(job))
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def scanMediaspaceDirectory(
        self,
        mediaspace,
        directory,
        recursive=False,
        create_proxies=True,
        scan_type="normal",
    ):
        # pylint:disable=too-many-arguments
        """Scan a directory within a mediaspace"""

        return self.scanMediaspaceInner(
            mediaspace, directory, recursive, create_proxies, scan_type
        )

    def scan_files(
        self,
        mediaspace,
        file_list,
        *,
        create_streaming_proxies=True,
        create_editing_proxies=False,
        update_pmr=False,
        full_scan=False,
        user="",
        password="",
        asset_uuid=None
    ):
        """Scan files with a single asset scan"""

        job = {
            "createproxy": "true" if create_streaming_proxies else "false",
            "create_editing_proxy": "true" if create_editing_proxies else "false",
            "mediaspace": mediaspace,
            "files": file_list,
            "update_pmr": "true" if update_pmr else "false",
            "fullscan": "true" if full_scan else "false",
            # 'metadata' : {
            #    'custom' : {
            #        "flow-story-export" : True
            #    }
            # }
        }

        if asset_uuid:
            job["metadata"] = {"asset_uuid": asset_uuid}

        if len(user) > 0:
            job["user"] = user

        if len(password) > 0:
            job["password"] = password

        reply = self.post("/scan/asset", json.dumps(job))
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def scanFile(
        self,
        mediaspace,
        files,
        create_proxies=True,
        update_pmr=False,
        user="",
        password="",
        asset_uuid=None,
    ):
        # pylint:disable=too-many-arguments
        """Scan files with a single asset scan"""
        return self.scan_files(
            mediaspace=mediaspace,
            file_list=files,
            create_streaming_proxies=create_proxies,
            update_pmr=update_pmr,
            user=user,
            password=password,
            asset_uuid=asset_uuid,
        )

    def getAssetScan(self, job_id):
        """Return an asset scan"""
        return self.getThatReturnsObj("/scan/asset/" + job_id)

    def getMediaspaceScan(self, job_id):
        """Returns the job status of the scan with job_id"""

        return self.getThatReturnsObj("/scan/mediaspace/" + job_id)

    def getScanResults(self, job_id):
        """Returns the job results"""

        return self.getThatReturnsObj("/scan/jobs/{}/results".format(job_id))

    def waitForSpaceScanToFinish(
        self, job_id, sleep_interval_secs=2, timeout_secs=3600
    ):
        """Helper to wait for a mediaspace scan job to finish"""

        return self.waitForJobToFinish(True, job_id, sleep_interval_secs, timeout_secs)

    def waitForFileScanToFinish(self, job_id, sleep_interval_secs=2, timeout_secs=3600):
        """Helper to wait for a file scan job to finish"""

        return self.waitForJobToFinish(False, job_id, sleep_interval_secs, timeout_secs)

    def wait_for_file_scan(self, job_id, sleep_interval_secs=2, timeout_secs=3600):
        """Helper to wait for a file scan job to finish"""

        return self.waitForJobToFinish(False, job_id, sleep_interval_secs, timeout_secs)

    def waitForJobToFinish(
        self, scanning_mediaspace, job_id, sleep_interval_secs=2, timeout_secs=3600
    ):
        """Helper to wait for a job to finish
        Waits for the scan job to complete
        Returns false if the job is not finished or fails
        Returns a list of asset IDs once complete
        """

        start = time.time()

        while True:

            if scanning_mediaspace:
                job = self.getMediaspaceScan(job_id)
            else:
                job = self.getAssetScan(job_id)

            logging.debug(
                "{0:.3f} waitForJobToFinish: {1}".format(
                    time.time() - start, job["state"]
                )
            )

            if job["state"] == "failed":
                logging.error("Scan job failed. %s", self.lastResponse())
                return False

            if job["state"] == "complete":
                # Return the asset IDs as a list when the scan completes
                if "asset_ids" not in job:
                    logging.error("Scan job failed. 'asset_ids' was not found")
                    return False
                return job["asset_ids"]

            time.sleep(sleep_interval_secs)

            if time.time() - start > timeout_secs:
                logging.error("Timeout waiting for scan job to finish")
                return False

    def get_workers(self):
        """Get all the registered workers"""

        return self.getThatReturnsObj("/scan/workers").json()

    def add_worker(self, host: str):
        """Add a scan worker"""

        add_worker_request = {
            "host": host,
        }
        return self.post("/scan/workers", json.dumps(add_worker_request))

    def remove_worker(self, host: str):
        """Remove a scan worker"""

        remove_worker_request = {
            "host": host,
        }
        return self.delete("/scan/workers", json.dumps(remove_worker_request))
