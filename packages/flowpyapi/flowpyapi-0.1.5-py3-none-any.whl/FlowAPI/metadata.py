"""
FLOW metadata service API
See here: https://developers.editshare.com/?urls.primaryName=EditShare%20FLOW%20Metadata
"""
import hashlib
import json
import logging
import os
import urllib.parse

from .core import (
    METADATA_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)


class Metadata(Connection):
    """Wraps the metadata service api"""

    # pylint: disable=too-many-public-methods,consider-using-f-string

    def __init__(self):
        super().__init__()
        self._service_name = "metadata"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Metadata, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr="127.0.0.1"):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Metadata, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        """Connect to service server"""

        return Connection.connect2(self, ip_addr, METADATA_PORT, username, password)

    def numClips(self):
        """Return the total number of clips in the system"""

        self.getThatReturnsObj("/clips?offset=0&limit=1")
        headers = self.lastReturnHeaders()
        for header in headers:
            if header[0].lower() == "x-total-count":
                return int(header[1])
        return False

    def createClip(self, data):
        """Create a new clip"""

        return self.postThatReturnsID("/clips", data)

    def clips(self, offset=0, limit=100):
        """Get a range of clips"""

        return self.getThatReturnsObj("/clips?offset={}&limit={}".format(offset, limit))

    def getClipsByIDs(self, id_list):
        """Get a list of clips from the supplied ids"""

        string_ints = [str(i) for i in id_list]
        return self.getThatReturnsObj("/clips?ids={}".format((",").join(string_ints)))

    def getFile(self, file_id):
        """Get information about a file"""

        return self.getThatReturnsObj("/files/" + str(file_id))

    def get_file_from_location_id(self, location_id):
        """Fetch a file from a location id"""

        return self.getThatReturnsObj("/files/?location_id={}".format(location_id))

    def getClip(self, clip_id):
        """Get information about a clip"""

        return self.getThatReturnsObj("/clips/" + str(clip_id))

    def getClipUNCData(self, clip_id):
        """Get unc information about a clip"""

        return self.getThatReturnsObj("/clips/" + str(clip_id) + "/unc")

    def getImage(self, image_id):
        """Get information about an image"""

        return self.getThatReturnsObj("/images/" + str(image_id))

    def getAsset(self, asset_id):
        """Get information about an asset"""

        return self.getThatReturnsObj("/assets/" + str(asset_id))

    def deleteClip(self, clip_id, delete_all=True):
        """Delete a clip"""

        url = "/clips/" + str(clip_id)
        if delete_all:
            url += "?all=true"
        self.delete(url)
        if self.lastReturnCode() != 200:
            return False
        return True

    def advancedDeleteClip(
        self,
        clip_id,
        online=False,
        metadata=False,
        archive=False,
        nearline=False,
        proxy=False,
        aaf=False,
    ):
        """Delete a clip"""
        # pylint: disable=too-many-arguments

        url = "/clips/" + str(clip_id)
        url += "?online=" + str(online).lower()
        url += "&metadata=" + str(metadata).lower()
        url += "&archive=" + str(archive).lower()
        url += "&nearline=" + str(nearline).lower()
        url += "&proxy=" + str(proxy).lower()
        url += "&aaf=" + str(aaf).lower()
        self.delete(url)
        if self.lastReturnCode() != 200:
            return False
        return True

    def deleteAsset(self, asset_id):
        """Delete an asset"""

        reply = self.delete("/assets/" + str(asset_id))
        return self.bool_from_reply("deleteAsset", reply)

    def createPlaceholder2(
        self, data, add_clip_to_project=True, create_project=True, create_sequence=True
    ):
        """Create a placeholder clip"""

        url = "/clips/placeholders?"
        if add_clip_to_project is True:
            url += "add-clip-to-project=true&"
        else:
            url += "add-clip-to-project=false&"

        # deprecated.  will be removed
        if create_project is True:
            url += "create-project=true&"
        else:
            url += "create-project=false&"

        # deprecated.  will be removed
        if create_sequence is True:
            url += "create-sequence=true&"
        else:
            url += "create-sequence=false&"

        return self.postThatReturnsID(url, data)

    def createPlaceholder(self, name, comment, space_name="", file_type="mov"):
        """Create a placeholder clip"""

        data = {
            "name": name,
            "comment": comment,
            "mediaspace": space_name,
            "filetype": file_type,
        }

        return self.createPlaceholder2(data)

    def createPlaceholder3(
        self, name, comment, space_name="", file_path="", file_type="mov"
    ):
        # pylint: disable=too-many-arguments
        """Create a placeholder clip"""

        url = "/clips/placeholders?"
        data = {
            "name": name,
            "comment": comment,
            "mediaspace": space_name,
            "file_path": file_path,
            "filetype": file_type,
        }

        return self.postThatReturnsID(url, data)

    def getCustomMetadataFields(self):
        """Get all custom metadata fields"""

        return self.getThatReturnsObj("/custom_metadata_fields")

    def update_custom_metadata_field(self, field_id, field_data):
        """Update a custom metadata field"""

        url = "/custom_metadata_fields/" + str(field_id)
        return self.putThatReturnsBOOL("update_custom_metadata_field", url, field_data)

    def getCustomMetadataField(self, field_id):
        """Get information about a custom metadata field"""

        return self.getThatReturnsObj("/custom_metadata_fields/" + str(field_id))

    def findCustomMetadataField(self, field_name):
        """Find a custom metadata field by it's name"""

        return self.find_custom_metadata_field_by_name(field_name)

    def find_custom_metadata_field_by_name(self, field_name):
        """Find a custom metadata field by it's name"""

        url = "/custom_metadata_fields?name="
        url += urllib.parse.quote(field_name)
        return self.getThatReturnsObj(url)

    def find_custom_metadata_field_by_db_key(self, db_key):
        """Find a custom metadata field by it's db key"""

        url = "/custom_metadata_fields?db_key="
        url += urllib.parse.quote(db_key)
        return self.getThatReturnsObj(url)

    def deleteCustomMetadataField(self, field_id):
        """Delete a custom metadata field"""

        return self.deleteThatReturnsBOOL(
            "deleteCustomMetadataField", "/custom_metadata_fields/" + str(field_id)
        )

    def createCustomMetadataField(self, data):
        """Create a custom metadata field"""

        reply = self.post("/custom_metadata_fields", json.dumps(data))
        if self.lastReturnCode() != 201:
            return False
        return json.loads(reply)

    def createCustomMetadataConfiguration(self, data):
        reply = self.post("/custom_metadata_configurations", json.dumps(data))
        if self.lastReturnCode() != 201:
            return False
        return json.loads(reply)

    def getCustomMetadataConfigurations(self):
        return self.getThatReturnsObj("/custom_metadata_configurations")

    def getSites(self):
        """Get a list of all sites"""

        return self.getThatReturnsObj("/sites")

    def createSite(self, data):
        """Create a site"""

        return self.postThatReturnsObj("/sites", data)

    def createSequence(self, data):
        """Create a sequence"""

        return self.postThatReturnsObj("/sequences", data)

    def cloneSequence(self, sequence_id):
        """Clone a sequence"""

        return self.postThatReturnsID("/sequences?source=" + str(sequence_id), "")

    def getSequence(self, sequence_id):
        """Get information about a sequence"""

        return self.getThatReturnsObj("/sequences/" + str(sequence_id))

    def deleteSequence(self, sequence_id):
        """Delete a sequence"""

        return self.deleteThatReturnsBOOL(
            "deleteSequence", "/sequences/" + str(sequence_id)
        )

    def updateSequence(self, sequence_id, data):
        """Update a sequence"""

        return self.putThatReturnsBOOL(
            "updateSequence", "/sequences/" + str(sequence_id), data
        )

    def updateClipStatus(
        self, clip_id, server_id, has_index=False, proxy_has_index=False
    ):
        """Update a clip's status"""

        clips = []

        if clip_id > 0:
            item = {
                "clip_id": clip_id,
                "has_index": has_index,
                "proxy_has_index": proxy_has_index,
            }
            clips.append(item)

        data = {"server_id": server_id}

        if clips:
            data["clips"] = clips

        return self.putThatReturnsBOOL("updateClipStatus", "/clips/status", data)

    def updateClip(self, clip_id, data):
        """Update a clip"""

        return self.putThatReturnsBOOL("updateClip", "/clips/" + str(clip_id), data)

    def lockSequence(self, sequence_id, lock):
        """Lock a sequence"""

        postfix = "?release=true"
        if lock:
            postfix = "?acquire=true"
        reply = self.put("/sequences/" + str(sequence_id) + postfix)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("lockSequence", reply)

    def userList(self):
        """Get a list of all users"""

        return self.getThatReturnsObj("/users")

    def getUser(self, user_id):
        """Get information about a user"""

        return self.getThatReturnsObj("/users/" + str(user_id))

    def findUser(self, username):
        """Find a user from a user name"""

        return self.getThatReturnsObj("/users?username=" + str(username))

    def createUser(self, user):
        """Create a new user"""

        return self.postThatReturnsObj("/users", user)

    def getProjects(self):
        """Create a list of all projects"""

        return self.getThatReturnsObj("/projects")

    def getProject(self, project_id):
        """Create information about a project"""

        reply = self.get("/projects/" + str(project_id))
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        return obj

    def findProject(self, name):
        """Find a project with the supplied name"""

        escaped_name = urllib.parse.quote(str(name))
        reply = self.get("/projects?name=" + escaped_name)
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        return obj

    def createProject(self, data):
        """Create a new project"""

        return self.postThatReturnsID("/projects", data)

    def deleteProject(self, project_id, really_delete=False):
        """Delete a project"""

        url = "/projects/" + str(project_id)
        if really_delete:
            url += "?force=true"
        return self.deleteThatReturnsBOOL("deleteProject", url)

    def updateProject(self, project_id, data):
        """Update a project"""
        return self.putThatReturnsBOOL(
            "updateProject", "/projects/" + str(project_id), data
        )

    def createSequenceEntry(self, data):
        return self.postThatReturnsID("/sequence_entries", data)

    def getSequenceEntry(self, entry_id):
        return self.getThatReturnsObj("/sequence_entries/" + str(entry_id))

    def ensureProjectExists(self, user, project_name):
        """Helper method to ensure a project exists"""

        project = self.findProject(project_name)
        if not project:
            project = {
                "is_public": False,
                "name": project_name,
                "owner_name": user,
            }
            project_id = self.createProject(project)
            return int(project_id)

        return int(project["project_id"])

    def getProjectFolders(self, project_id):
        return self.getThatReturnsObj(
            "/projects/{}?folders=true".format(str(project_id))
        )

    def getProjectContents(self, project_id):
        return self.getThatReturnsObj(
            "/projects/{}?contents=true".format(str(project_id))
        )

    def createProjectFolder(self, project_id, parent_id, folder_name):

        data = {
            "name": folder_name,
            "project_id": project_id,
            "parent_folder_id": parent_id,
        }

        return self.postThatReturnsID("/project_folders", data)

    def getProjectFolder(self, folder_id):
        return self.getThatReturnsObj("/project_folders/{}".format(str(folder_id)))

    def updateProjectFolder(self, folder_id, data):
        return self.putThatReturnsBOOL(
            "updateProjectFolder", "/project_folders/" + str(folder_id), data
        )

    def deleteProjectFolder(self, folder_id):
        return self.deleteThatReturnsBOOL(
            "deleteProjectFolder", "/project_folders/" + str(folder_id)
        )

    def ensureProjectFolderExists(self, project_id, folder_name):

        fid = -1
        folder_list = self.getProjectFolders(project_id)
        if not folder_list:
            fid = -1
        else:
            for entry in folder_list:
                if entry["folder"]["name"] == folder_name:
                    fid = entry["folder"]["project_folder_id"]
                    break

        # do we need to create
        if fid < 1:
            fid = self.createProjectFolder(project_id, -1, folder_name)
        return fid

    def createProjectClipEntry(self, clip_id):
        data = {"clip_id": clip_id}

        return self.postThatReturnsID("/project_clips", data)

    def getProjectClipEntry(self, item_id):
        return self.getThatReturnsObj("/project_clips/{}".format(str(item_id)))

    def addClipToProjectFolder(self, project_id, parent_folder_id, clip_id):

        eid = self.createProjectClipEntry(clip_id)
        # print(self.getProjectClipEntry( eid ))

        data = {
            "project_id": project_id,
            "parent_folder_id": parent_folder_id,
            "project_clip_id": eid,
            "clip_id": clip_id,
        }

        return self.postThatReturnsID("/project_entries", data)

    def updateCapture(self, capture_id, data):
        return self.putThatReturnsBOOL(
            "updateCapture", "/captures/" + str(capture_id), data
        )

    def updateAsset(self, asset_id, data):
        return self.putThatReturnsBOOL("updateAsset", "/assets/" + str(asset_id), data)

    def updateClipMetadata(self, metadata_id, data):
        return self.putThatReturnsBOOL(
            "updateClipMetadata", "/metadata/" + str(metadata_id), data
        )

    def getFileSizes(self, data):
        reply = self.getWithData("/files/sizes", json.dumps(data))
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        return obj

    def createSharedResource(self, name, filename, filesize, resource_type):
        data = {
            "filename": filename,
            "filesize": filesize,
            "name": name,
            "type": resource_type,
        }
        return self.postThatReturnsObj("/shared_resources", data)

    def deleteSharedResource(self, resource_id):
        return self.deleteThatReturnsBOOL(
            "deleteSharedResource", "/shared_resources/" + str(resource_id)
        )

    def getSharedResource(self, resource_id):
        return self.getThatReturnsObj("/shared_resources/" + str(resource_id))

    def getSharedResourceByName(self, resource_name):
        return self.getThatReturnsObj("/shared_resources?name=" + str(resource_name))

    def getSharedResourceByType(self, resource_type):
        return self.getThatReturnsObj("/shared_resources?type=" + str(resource_type))

    @staticmethod
    def calculateFlowHash(file_path):
        """Helper method to calculate the Flow hash of a file"""

        if not os.path.exists(file_path):
            logging.warning("calculateFlowHash: '%s' does not exist", file_path)
            return False

        file_size = os.path.getsize(file_path)
        hasher = hashlib.md5()

        with open(file_path, "rb") as file_handle:

            block_size = 4 * 1024

            if file_size > (24 * block_size):
                # start block
                hasher.update(file_handle.read(4 * block_size))

                # middle block
                file_handle.seek((file_size - 4 * block_size) / 2)
                hasher.update(file_handle.read(4 * block_size))

                # end block.  read a bit more from the end as various programs
                # tag extra data on the end
                file_handle.seek(file_size - 8 * block_size)
                hasher.update(file_handle.read(8 * block_size))

                # add the file size as well - string equivalent of size, base 10
                # i.e. 1234 --> "1234"
                hasher.update("{}".format(file_size))

            else:
                hasher.update(file_handle.read())

        return "2:" + hasher.hexdigest()

    def createFile(self, data):
        """Create a file"""
        reply = self.post("/files", json.dumps(data))
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def deleteLocation(self, file_id, mediaspace_location_id):
        """Delete a location"""
        return self.deleteThatReturnsBOOL(
            "deleteLocation",
            "/files/" + str(file_id) + "?location_id=" + str(mediaspace_location_id),
        )

    def addLocation(self, flow_hash, location):
        """Add a new location for a file"""
        data = {"file": {"hash": flow_hash}, "locations": [location]}
        return self.postThatReturnsID("/files", data)

    def create_log_entry(self, data):
        """Create a new log entry"""
        return self.postThatReturnsID("/log_entries", data)

    def create_log_entries(self, list_of_entries):
        """Creates a new log entries from a list"""
        return self.postThatReturnsObj("/log_entries", list_of_entries)

    def createLogEntry(self, data):
        """Create a new log entry"""
        return self.create_log_entry(data)

    def get_log_entries(self, capture_id):
        """Create all log entries for a capture"""
        url = "/log_entries?capture_id="+str(capture_id)
        response = self.getThatReturnsObj(url)
        if not response:
            response = []
        return response

    def delete_log_entry(self, log_entry_id):
        """Delete a log entry"""
        return self.deleteThatReturnsBOOL("delete_log_entry", "/log_entries/" + str(log_entry_id))

    def getMarker(self, marker_id):
        """Get a marker"""
        return self.getThatReturnsObj("/markers/" + str(marker_id))

    def createMarker(self, data):
        """Create a marker"""
        return self.postThatReturnsID("/markers", data)

    def createMarker2(self, capture_id, color, time, comment):
        """Create a marker"""

        data = {
            "capture_id": capture_id,
            "color": color,
            "time": time,
            "comment": comment,
        }

        return self.postThatReturnsID("/markers", data)

    def updateMarker(self, marker_id, data):
        """Edit a marker"""

        return self.putThatReturnsBOOL(
            "updateMarker", "/markers/" + str(marker_id), data
        )

    def deleteMarker(self, marker_id):
        """Delete a marker"""

        return self.deleteThatReturnsBOOL("deleteMarker", "/markers/" + str(marker_id))

    def getSequenceMarkers(self, sequence_id):
        """Get all sequence markers for a sequence"""

        return self.getThatReturnsObj(
            "/sequence_markers?sequence_id=" + str(sequence_id)
        )

    def getSequenceMarker(self, sequence_marker_id):
        """Get a new sequence marker"""

        return self.getThatReturnsObj("/sequence_markers/" + str(sequence_marker_id))

    def createSequenceMarker(self, data):
        """Create a new sequence marker"""

        return self.postThatReturnsID("/sequence_markers", data)

    def updateSequenceMarker(self, sequence_marker_id, data):
        """Edit a sequence marker"""

        return self.putThatReturnsBOOL(
            "updateSequenceMarker", "/sequence_markers/" + str(sequence_marker_id), data
        )

    def deleteSequenceMarker(self, sequence_marker_id):
        """Delete a sequence marker"""

        return self.deleteThatReturnsBOOL(
            "deleteSequenceMarker", "/sequence_markers/" + str(sequence_marker_id)
        )

    def createSubclip(self, master_id, name, timecode_in, timecode_out, uuid=None):
        # pylint: disable=too-many-arguments
        """Create a new subclip"""

        data = {
            "timecode_in": timecode_in,
            "timecode_out": timecode_out,
        }
        if name and len(name) > 0:
            data["clip_name"] = name

        if uuid:
            data["asset_uuid"] = str(uuid)

        return self.postThatReturnsID("/clips/{}/subclip".format(master_id), data)

    @staticmethod
    def secondsFromTC(timecode):
        """Helper to return number of seconds in a timecode.
        Input should be like this '00:00:13:19:24000/1001'
        """

        items = timecode.split(":")
        if len(items) != 5:
            logging.error("secondsFromTC: '%s' invalid", timecode)
            return False

        # calculate rate
        ritems = items[4].split("/")
        rate = float(ritems[0]) / float(ritems[1])

        hours = int(items[0])
        mins = int(items[1])
        secs = int(items[2])
        frames = int(items[3])

        dec = frames / rate
        # print( rate )
        # print( dec )
        return (hours * 3600) + (mins * 60) + secs + dec

    def getEvents(self, start, count):
        """Get system events"""
        # start=10&max_events=100&sort_by=user&sort_order=DESC
        return self.getThatReturnsObj(
            "/events?start={}&max_events={}&sort_by=time&sort_order=ASC".format(
                start, count
            )
        )

    def get_asset_associations_ids(self, asset_id):
        """Get a list of associated asset ids"""
        return self.getThatReturnsObj(
            "/assets/{}/associations?ids_only=true".format(asset_id)
        )

    def clip_add_child(self, parent_id, child_id):
        """Add a child parent relationship"""
        url = "/clips/{}/parent_clip/{}".format(child_id, parent_id)
        return self.post(url, None)
