"""FlowAPI / RenderMaster"""
import json
import logging
import time

from .core import (
    RENDERMASTER_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)
from .metadata import Metadata


class RenderMaster(Connection):
    """Wraps the render master service api"""

    # pylint: disable=consider-using-f-string

    def __init__(self):
        super().__init__()
        self._service_name = "rendermaster"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(RenderMaster, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr="127.0.0.1"):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(RenderMaster, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        """Connect to api server"""

        return Connection.connect2(self, ip_addr, RENDERMASTER_PORT, username, password)

    def createJob(self, job):
        reply = self.post("/rendermaster/jobs", json.dumps(job))
        # print reply
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def create_proxy_for_clip_job(self, clip_id: int):
        """Create a proxy for a clip"""

        metadata = Metadata.create_instance(self._ip, self._username, self._password)
        clip_data = metadata.getClip(clip_id)
        # print(json.dumps(clip_data, indent=2))

        if "video" not in clip_data:
            return False

        video_info = clip_data["video"][0]

        location = None
        for loc in video_info["file"]["locations"]:
            if loc["archive"]:
                continue
            location = loc
            break

        # may not be online
        if not location:
            return False

        job_data = {
            "clip_data": {
                "clip_id": clip_data["clip_id"],
                "source_media_space": location["media_space_uuid"],
                "clip_name": clip_data["metadata"]["clip_name"],
                "file_type": video_info["file"]["file"]["type"],
                "frame_height": video_info["height"],
                "frame_width": video_info["width"],
                "start_timecode": video_info["timecode_start"],
                "tape_name": clip_data["capture"]["tape"],
                "video_path": "Content/" + location["userpath"],
                "user": "mhallin"
                # "duration_seconds": "30",
            },
            "request_type": "RenderClipProxyFromScan",
        }

        return self.createJob(job_data)

    def registerWorker(self, host_ip):
        data = {"host": host_ip}

        reply = self.post("/rendermaster/workers", json.dumps(data))
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def removeWorker(self, host_ip):
        data = {"host": host_ip}

        reply = self.delete("/rendermaster/workers", json.dumps(data))
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def getWorkers(self):
        return self.get("/rendermaster/workers")

    def getJob(self, job_id):
        return self.getThatReturnsObj("/rendermaster/jobs/" + job_id)

    def getAllJobs(self):
        return self.getThatReturnsObj("/rendermaster/jobs")

    def deleteJob(self, job_id):
        reply = self.delete("/rendermaster/jobs/" + job_id)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("deleteProxyWorkerJob", reply)

    def waitForJobToFinish(self, job_id, sleep_interval_secs=2, timeout_secs=3600):
        """Waits for the job to complete, returns false if the job is not finished or fails"""

        start = time.time()

        while True:

            job = self.getJob(job_id)

            if self.lastReturnCode() != 200:
                logging.error(
                    "Failed to get job! code: %s response: %s",
                    self.lastReturnCode(),
                    self.lastResponse(),
                )
                return False

            logging.debug(
                "waitForJobToFinish: time: {0:.2f} progress: {1:} state: {2:}".format(
                    time.time() - start, job["progress"], job["state"]
                )
            )

            if job["state"] == "failed":
                logging.error("Rendermaster job failed. %s", self.lastResponse())
                return False

            if job["state"] == "complete":
                return True

            time.sleep(sleep_interval_secs)

            if time.time() - start > timeout_secs:
                logging.error("Timeout waiting for rendermaster job to finish")
                return False
