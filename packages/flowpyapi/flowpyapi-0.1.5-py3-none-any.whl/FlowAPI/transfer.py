"""
FLOW Transfer service API
See here: https://developers.editshare.com
"""
import logging
import os
import uuid

from .core import (
    TRANSFER_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)


class Transfer(Connection):
    """Wraps the Transfer server api"""

    # pylint: disable=too-many-public-methods,consider-using-f-string

    def __init__(self):
        super().__init__()
        self._service_name = "transfer"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Transfer, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr="127.0.0.1"):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Transfer, username, password, ip_addr)

    # Connect to server
    def connect(self, ip_addr, username, password):
        return Connection.connect2(self, ip_addr, TRANSFER_PORT, username, password)

    def createDownloadJob(self, data):
        return self.postThatReturnsObj("/transfer/download", data)

    def deleteDownloadJob(self, job_id):
        reply = self.delete("/transfer/download/" + job_id)
        return self.bool_from_reply("deleteDownloadJob", reply)

    def downloadFile(
        self, file_id, dst_filename, overwrite_existing=True, chunk_size=5 * 0x100000
    ):
        # pylint: disable=too-many-locals

        if os.path.isfile(dst_filename):
            os.remove(dst_filename)

        data = {"file_id": file_id}

        job = self.createDownloadJob(data)
        if not job:
            # print( self.lastResponse() )
            return False

        # print( job )

        job_id = job[0]["transfer"]
        url = "/download/" + job_id
        if self._use_gateway:
            url = self._gateway_prefix + self._service_name + url

        # print( url )

        file_handle = open(dst_filename, "wb")

        done = 0
        size = job[0]["file_size_bytes"]
        return_result = True

        while done != size:

            bytes_left = size - done
            bytes_to_get = chunk_size
            if bytes_to_get > bytes_left:
                bytes_to_get = bytes_left

            # format headers
            our_headers = {
                "Authorization": self._basic_auth_data,
                "Range": "bytes={}-{}".format(done, done + bytes_to_get),
            }
            # print( h )

            self._conn.request("GET", url, body=None, headers=our_headers)

            response = self._conn.getresponse()

            # print( response.status )
            # print( response.getheader('content-range') )

            content = response.read()
            file_handle.write(content)
            done += len(content)

        file_handle.close()
        if not return_result:
            os.remove(dst_filename)

        self.deleteDownloadJob(job_id)
        return return_result

    def getStorageCapabilities(self):
        return self.getThatReturnsObj("/transfer/storage/capabilities/")

    def getStorageCapabilitiesAsCsv(self):
        return self.getThatReturnsObj("/transfer/storage/capabilities?csv=true")

    def startConnectionTest(self, data):
        return self.postThatReturnsObj("/transfer/test/", data)

    def getConnectionTest(self, job_id):
        return self.getThatReturnsObj("/transfer/test/" + str(job_id))

    def deleteConnectionTest(self, job_id):
        return self.deleteThatReturnsBOOL(
            "deleteConnectionTest", "/transfer/test/" + str(job_id)
        )

    def createUploadJob(self, data):
        return self.postThatReturnsObj("/transfer/upload", data)

    def uploadChunk(self, job_id, data):
        reply = self.put("/transfer/upload_chunked/" + str(job_id), data)
        if self.lastReturnCode() != 200:
            return False
        return reply

    def uploadFinialize(self, job_id):
        reply = self.post("/transfer/upload_chunked/" + str(job_id) + "/finalise", "")
        if self.lastReturnCode() != 200:
            return False
        return reply

    def deleteUploadJob(self, job_id):
        return self.deleteThatReturnsBOOL(
            "deleteUploadJob", "/transfer/upload/" + str(job_id)
        )

    def uploadFile(
        self,
        src_file_path,
        dst_media_space,
        dst_file_path,
        resource_type="asset",
        chunk_size=5 * 0x100000,
        do_scan=True,
        create_proxy=True,
        update_pmr=True,
    ):
        # pylint: disable=too-many-arguments,too-many-locals

        file_size = os.stat(src_file_path).st_size

        if resource_type == "shared":
            dst_file_path = "%s.bin" % str(uuid.uuid4())

        job_data = {
            "resource_type": resource_type,
            "file_path": dst_file_path,
            "scan": do_scan,
            "create_proxy": create_proxy,
            "update_pmr": update_pmr,
            "file_size_bytes": file_size,
            "user": self._username,
        }

        if resource_type != "asset":
            job_data["scan"] = False
            job_data["create_proxy"] = False
            job_data["update_pmr"] = False

        if dst_media_space:
            job_data["mediaspace"] = dst_media_space

        print(job_data)
        job = self.createUploadJob(job_data)
        if not job:
            # print( self.lastResponse() )
            return False

        # print( job )
        job_id = job[0]["transfer"]

        file_handle = open(src_file_path, "rb")

        return_result = True

        while True:

            # toRead = chunk_size
            # if done + chunk_size > file_size:
            #    toRead = file_size-done

            data = file_handle.read(chunk_size)
            if not data:
                logging.error("uploadFile: Failed to read from file.")
                return False

            total_bytes = self.uploadChunk(job_id, data)
            if not total_bytes:
                logging.error(
                    "uploadFile: Failed to upload data chunk. %s", self.lastResponse()
                )
                return_result = False
                break

            # print( "upload res={}".format( total_bytes ) )
            # print( "pos=%d" % fh.tell() )
            logging.debug(
                "total_bytes=%d file_size=%d", int(total_bytes), int(file_size)
            )

            if int(total_bytes) == int(file_size):
                break

        file_handle.close()
        res = self.uploadFinialize(job_id)
        if not res:
            logging.error(
                "uploadFile: Failed to finialize upload. %s", self.lastResponse()
            )
            return_result = False

        # res = self.deleteUploadJob( job_id )
        # if res == False:
        #    logging.error( "uploadFile: Failed to delete upload job. %s" % self.lastResponse() )
        #    rv = False

        if not return_result:
            return False

        return job[0]

    def uploadResourceFile(
        self,
        local_file_path,
        remote_file_path,
        resource_type="shared",
        chunk_size=5 * 0x100000,
    ):
        return self.uploadFile(
            local_file_path, None, remote_file_path, resource_type, chunk_size
        )

    def copy(self, data):
        return self.postThatReturnsObj("/transfer/copy", data)

    def getCopyJob(self, job_id, short_status=False):
        endpoint = "/transfer/copy/" + job_id
        if short_status:
            endpoint += "?shortstatus=true"
        return self.getThatReturnsObj(endpoint)

    def getCopyJobs(self):
        return self.getThatReturnsObj("/transfer/copy/")

    def deleteCopyJob(self, job_id):
        return self.deleteThatReturnsBOOL(
            "deleteCopyJob", "/transfer/copy/" + str(job_id)
        )

    def move(self, data):
        return self.postThatReturnsObj("/transfer/move", data)

    def getMoveJob(self, job_id):
        return self.getThatReturnsObj("/transfer/move/" + job_id)

    def getMoveJobs(self):
        return self.getThatReturnsObj("/transfer/move/")

    def deleteMoveJob(self, job_id):
        return self.deleteThatReturnsBOOL(
            "deleteMoveJob", "/transfer/move/" + str(job_id)
        )

    def deleteFile(self, data):
        return self.postThatReturnsObj("/transfer/delete", data)

    def getDeleteJob(self, job_id):
        return self.getThatReturnsObj("/transfer/delete/" + job_id)

    def getDeleteJobs(self):
        return self.getThatReturnsObj("/transfer/delete/")

    def deleteDeleteJob(self, job_id):
        return self.deleteThatReturnsBOOL(
            "deleteDeleteJob", "/transfer/delete/" + str(job_id)
        )
