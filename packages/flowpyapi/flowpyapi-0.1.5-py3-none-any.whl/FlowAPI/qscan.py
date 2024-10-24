# FlowAPI / QScan
import datetime
import json
import logging
import time
import uuid
from base64 import b64encode

from .core import Connection


class QScan(Connection):
    """Wraps the QScan server"""

    # Connect to api server
    def connect(self, ip, username, password):
        port = 8080
        Connection.connect(self, ip, port)

        # we need to base 64 encode it
        # and then decode it to acsii as python 3 stores it as a byte string
        userpass = username + ":" + password
        userAndPass = b64encode(userpass.encode()).decode()
        # self._headers = { 'Authorization' : 'Basic %s' %  userAndPass }
        self._basic_auth_data = "Basic %s" % userAndPass
        self._username = username
        self._password = password
        self._ip = ip
        self._port = port
        self._content_type = "application/json"

    # Old API requests

    def pauseProject(self, id):
        rv = self.postThatReturnsObj("/api-1/projects/pause/{}.json".format(id), None)
        return rv

    def resumeProject(self, id):
        rv = self.postThatReturnsObj("/api-1/projects/resume/{}.json".format(id), None)
        return rv

    def findProject(self, name):
        projectList = self.getProjects()
        if not projectList:
            return False

        for project in projectList["projects"]:
            projectName = project["Project"]["name"]
            if projectName == name:
                return project

        return False

    def createProject(self, data):
        rv = self.postThatReturnsObj("/api-1/projects.json", data)
        return rv

    def getProjectStatus(self, id):
        rv = self.getThatReturnsObj("/api-1/projects/status/{}.json".format(id))
        return rv

    def deleteProject(self, id):
        reply = self.delete("/api-1/projects/{}.json".format(id))
        # print(reply)
        # returns something like this:
        # {"result":true,"message":"Project is being deleted"}
        if self.lastReturnCode() != 200:
            return False
        return True

    def getAnalysisProfiles(self):
        rv = self.getThatReturnsObj("/api-1/analysisprofiles.json")
        return rv

    def getAnalysisProfile(self, id):
        rv = self.getThatReturnsObj("/api-1/analysisprofiles/{}.json".format(id))
        return rv

    def getTemplate(self, templateID):
        rv = self.getThatReturnsObj(
            "/api-1/analysisprofiles/{}.json".format(templateID)
        )
        return rv

    def getAllProjects(self):
        rv = self.getThatReturnsObj("/api-1/projects.json")
        return rv

    def getFileInfo(self, fileID):
        rv = self.getThatReturnsObj("/api-1/pfiles/fileinfo/{}.json".format(fileID))
        return rv

    def restartProject(self, data, projectID):
        rv = self.postThatReturnsObj(
            "/api-1/projects/resume/{}.json".format(projectID), data
        )
        return rv

    # New API requests

    def createRepository(self, data):
        rv = self.postThatReturnsObj("/api-1/qc/repositories", data)
        return rv

    def getAllRepositories(self):
        rv = self.getThatReturnsObj("/api-1/qc/repositories")
        return rv

    def findRepoForFile(self, uncPath):
        list = self.getAllRepositories()
        if not list:
            return False

        pathF = uncPath.replace("\\", "/")
        for i in list:
            # print i
            if "path" in i and len(i["path"]) > 2:
                if pathF.startswith(i["path"]):
                    # print(pathF)
                    return i

        return False

    def createJob(
        self, jobName, jobDescription, templateID, files, analysisPerformance=10
    ):

        if not files:
            return False

        if len(files) < 1:
            return False

        repo = self.findRepoForFile(files[0])
        if not repo:
            logging.error("Failed to find repo for file")
            return False

        list = []
        for i in files:
            kd = {
                "repository_id": repo["id"],
                # "path" : i,
                "full_path": i,
            }
            list.append(kd)

        """
        analysis_performance values
        " 1 - Slow";
        " 5 - Medium";
        "10 - Full speed";
        "15 - Very high speed";
        """

        if not jobName:
            jobName = datetime.datetime.now().strftime(
                "Flow-QScan-Api-%Y-%m-%d-%H-%M-%S"
            )
            # jobName = str(uuid.uuid4())

        if not jobDescription:
            jobDescription = "Flow Python API"

        job = {
            "name": jobName,
            "analysis_performance": analysisPerformance,
            # "all_nodes" : 1,
            "description": str(jobDescription),
            "template_id": str(templateID),
            "files": list,
        }

        # print json.dumps( job, sort_keys=True, indent=2, separators=(',', ': '))
        # print( json.dumps( job ))
        reply = self.post("/api-1/qc/jobs", json.dumps(job))
        # print reply
        if self.lastReturnCode() != 200:
            logging.error(
                "Failed to create job code:{} {}".format(
                    self.lastReturnCode(), self.lastResponse()
                )
            )
            return False

        logging.debug("Created qscan job '{}'".format(jobName))
        # print reply
        try:
            obj = json.loads(reply)
        except Exception as e:
            logging.error("" + str(e))
            return False

        if not self.resumeJob(obj):
            return False

        # Waits for the job to start
        start = time.time()
        sleepIntervalSecs = 2
        timeoutSecs = 120

        while True:

            status = self.getJobState(obj)
            logging.debug(status)

            logging.debug(
                "{0:.3f} waitForJobToStart: {1}".format(
                    time.time() - start, status["status"]
                )
            )

            if status["status"] == "running":
                break

            time.sleep(sleepIntervalSecs)

            if time.time() - start > timeoutSecs:
                logging.error("Timeout waiting for job to start")
                return False

        return obj

    def bool_from_reply2(self, func, reply):

        # print( "bool_from_reply2", reply )
        if len(reply) == 0:
            return False
        obj = json.loads(reply)
        # print( "reply=", rv )
        if "status" not in obj:
            logging.warning(func + " failed:", reply)
            return False
        return obj["status"] == "Ok"

    def pauseJob(self, job):
        reply = self.put("/api-1/qc/jobs/{}/pause".format(job["id"]))
        return self.bool_from_reply2("pauseJob", reply)

    def resumeJob(self, job):
        reply = self.put("/api-1/qc/jobs/{}/resume".format(job["id"]))
        return self.bool_from_reply2("resumeJob", reply)

    def deleteJob(self, job):
        reply = self.delete("/api-1/qc/jobs/{}".format(job["id"]))
        return self.bool_from_reply2("deleteJob", reply)

    # def getJob( self, jobId ):
    #    rv = self.getThatReturnsObj( '/renders/jobs/' + jobId )
    #    return rv

    def getJobState(self, job):
        rv = self.getThatReturnsObj("/api-1/qc/jobs/{}/status".format(job["id"]))
        return rv

    def version(self):
        rv = self.getThatReturnsObj("/api-1/qc/version")
        return rv

    def ping(self):
        rv = self.getThatReturnsObj("/api-1/qc/ping")
        # print(rv)
        return rv

    def getFileStatus(self, jobID, fileID):
        rv = self.getThatReturnsObj(
            "/api-1/qc/jobs/{}/files/{}/status".format(jobID, fileID)
        )
        return rv

    def getProjects(self):
        rv = self.getThatReturnsObj("/api-1/projects.json")
        return rv

    def getFileEvents(self, jobID, fileID, severity=None):
        url = "/api-1/qc/jobs/{}/files/{}/events".format(jobID, fileID)
        if severity:
            url += "?severity=" + severity
        rv = self.getThatReturnsObj(url)
        return rv

    # Helper to wait for a job to finish
    def waitForJobToFinish(self, job, sleepIntervalSecs=2, timeoutSecs=3600):

        # Waits for the scan job to complete, returns false if the job is not finished or fails
        start = time.time()

        while True:

            status = self.getJobState(job)
            # logging.debug( status )

            if not status:
                logging.error(
                    "Failed to get job state id:{} {} {}".format(
                        job["id"], self.lastReturnCode(), self.lastResponse()
                    )
                )
                return False

            logging.debug(
                "{0:.3f} waitForJobToFinish: id:{1} status:{2}".format(
                    time.time() - start, job["id"], status["status"]
                )
            )

            if status["status"] != "running":
                return False

            allDone = True
            for file in job["files"]:

                # fevents = self.getFileEvents( job["id"], file["id"] )
                # print(fevents)

                fstatus = self.getFileStatus(job["id"], file["id"])
                if not fstatus:
                    logging.error(
                        "Failed to get file status id:{} {} {}".format(
                            file["id"], self.lastReturnCode(), self.lastResponse()
                        )
                    )
                    # allDone = False
                else:
                    logging.debug("File Status: '{}'".format(fstatus["status"]))
                    # print(fstatus)
                    # if fstatus["status"] == "analyzing" or fstatus["status"] == "initializing" or fstatus["status"] == "ready" or fstatus["status"] == "queued":
                    if fstatus["status"] == "error":
                        logging.error(
                            "File id:{} status:{}".format(file["id"], fstatus["status"])
                        )
                        print(fstatus)
                    elif fstatus["status"] == "unsupported":
                        pass
                    elif fstatus["status"] == "analysis_error":
                        pass
                    elif fstatus["status"] != "analyzed":
                        allDone = False
                        break

            if allDone:
                return True
            """
            if( status['status'] == 'failed' ):
                logging.error( "QScan job failed. " + self.lastResponse() )
                return False
            
            if( job['state'] == 'complete' ):
                # Return the asset IDs as a list when the scan completes
                if 'asset_ids' not in job:
                    logging.error( "Scan job failed. 'asset_ids' was not found" )
                    return False
                return job['asset_ids']
            """
            time.sleep(sleepIntervalSecs)

            if time.time() - start > timeoutSecs:
                logging.error("Timeout waiting for qscan job to finish")
                return False
