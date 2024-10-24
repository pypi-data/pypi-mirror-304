"""
FlowAPI / EditShare Storage service API
See here: https://developers.editshare.com/?urls.primaryName=EditShare%20Storage
"""
import base64
import logging
import urllib.parse

from .core import Connection, create_gateway_instance_inner, create_instance


class EditShare(Connection):
    """Wraps the EditShare Storage Service API"""

    # pylint: disable=too-many-public-methods,consider-using-f-string

    def __init__(self):
        super().__init__()
        self._service_name = "storage"

    @staticmethod
    def create_gateway_instance(username, password, ip_addr="127.0.0.1"):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(EditShare, username, password, ip_addr)

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(EditShare, ip_addr, username, password)

    def connect(self, ip_addr, username, password):
        """Connect to service"""

        self._content_type = "application/json"
        return Connection.connect2(self, ip_addr, 8083, username, password)

    def get_bit_buckets(self):
        """Get all bit buckets"""

        return self.getThatReturnsObj("/v1/bitbuckets")

    def get_spaces(self):
        """Get all spaces"""

        return self.getThatReturnsObj("/v1/spaces")

    def get_space(self, name):
        """Get information about a mediaspace"""

        return self.getThatReturnsObj(urllib.parse.quote("/v1/spaces/" + name))

    def space_exists(self, name):
        """Does a space exist?"""

        space = self.get_space(name)
        if not space:
            return False
        return True

    def create_space(self, ms_name, ms_type, quota=107374182400):
        """Create a new media space
        ms_type: one of avidmxf, managed, unmanaged, universal, avidstyle, acl
        """
        data = {
            "space_name": ms_name,
            "type": "media",
            "subtype": ms_type,
            "quota": quota,
        }
        return self.postThatReturnsObj("/v1/spaces", data)

    def delete_space(self, name, save_to_trash=True):
        """Delete a media space"""

        stt = "true"
        if not save_to_trash:
            stt = "false"
        return self.delete("/v1/spaces/{}?save_media_to_trash={}".format(name, stt))

    def get_groups(self):
        """Get all user groups"""

        return self.getThatReturnsObj("/v1/groups")

    def delete_group(self, name, save_to_trash=True):
        """Delete a user group"""

        stt = "true"
        if not save_to_trash:
            stt = "false"
        return self.delete("/v1/groups/{}?save_media_to_trash={}".format(name, stt))

    def get_users(self):
        """Get all users"""

        return self.getThatReturnsObj("/v1/users")

    def get_user(self, name):
        """Get user information"""

        return self.getThatReturnsObj("/v1/users/" + name)

    def user_exits(self, name):
        """Does the username exist?"""

        user = self.get_user(name)
        if not user:
            return False
        return True

    def create_user(self, username, password):
        """Create a new user"""

        data = {"username": username, "password": password}
        return self.postThatReturnsObj("/v1/users", data)

    def delete_user(self, name, save_to_trash=True):
        """Delete a user"""

        stt = "true"
        if not save_to_trash:
            stt = "false"
        return self.delete("/v1/users/{}?save_media_to_trash={}".format(name, stt))

    def get_space_users(self, spacename):
        """Get all users in a space"""

        return self.getThatReturnsObj(
            urllib.parse.quote("/v1/spaces/{}/users".format(spacename))
        )

    def add_user_to_space(self, spacename, username, read_only=False):
        """Add a user to a space"""

        data = {"username": username, "readonly": read_only}
        return self.postThatReturnsObj("/v1/spaces/{}/users".format(spacename), data)

    def is_user_in_space(self, username, spacename):
        """Is the user a member of the space?"""

        users = self.get_space_users(spacename)

        for user in users:
            if user["username"] == username:
                return True
        return False

    def create_user_and_space(
        self, username, password, spacename, spacetype, delete_if_exists, to_trash
    ):
        # pylint: disable=too-many-arguments
        """
        Helper to create a user and space and add the user to the space
        If delete_if_exists is true then we remove existing space/user first
        """

        create_space = False
        if self.space_exists(spacename):
            logging.debug("space '%s' exists", spacename)
            if delete_if_exists:
                logging.debug("Deleting space '%s'", spacename)
                self.delete_space(spacename, to_trash)
                create_space = True
        else:
            create_space = True

        if create_space:
            logging.debug("Creating space '%s'", spacename)
            self.create_space(spacename, spacetype)

        create_user = False

        if self.user_exits(username):
            logging.debug("user '%s' exists", username)
            if delete_if_exists:
                logging.debug("Deleting user '%s'", username)
                self.delete_user(username, to_trash)
                create_user = True
        else:
            create_user = True

        if create_user:
            logging.debug("Creating user '%s'", username)
            self.create_user(username, password)

        if not self.is_user_in_space(username, spacename):
            self.add_user_to_space(spacename, username)

    def get_object_storage_buckets(self):
        """Get a list of available storage buckets"""

        return self.getThatReturnsObj("/v1/object-storage/buckets")

    def create_object_storage_bucket(self, data):
        """TODO - find out what this does"""

        return self.postThatReturnsObj(
            "/v1/object-storage/buckets?skip_access_validation=true", data
        )

    def remove_object_storage_bucket(self, item_id):
        """Add a storage bucket - TODO eloborate"""

        return self.delete("/v1/object-storage/buckets/{}".format(item_id))

    def get_object_storage_links(self, spacename=None):
        """TODO - find out what this does"""

        if spacename:
            return self.getThatReturnsObj(
                "/v1/spaces/{}/object-storage/links".format(spacename)
            )
        return self.getThatReturnsObj("/v1/object-storage/links")

    def create_object_storage_link(self, spacename, data):
        """TODO - find out what this does"""

        return self.postThatReturnsObj(
            "/v1/spaces/{}/object-storage/links".format(spacename), data
        )

    def remove_object_storage_link(self, spacename, item_id):
        """TODO - find out what this does"""

        return self.delete(
            "/v1/spaces/{}/object-storage/links{}".format(spacename, item_id)
        )

    def get_media_proxy_links(self, spacename, linkname):
        """Get proxy links"""

        enc = base64.b64encode(linkname.encode())
        return self.getThatReturnsObj(
            "/v1/spaces/{}/media_proxies/{}".format(spacename, enc)
        )

    def create_media_proxy_link(self, spacename, linkname, efspath):
        """Link a media proxy file"""

        data = {"efs_path": efspath, "link_name": linkname}
        return self.postThatReturnsObj(
            "/v1/spaces/{}/media_proxies".format(spacename), data
        )

    def disable_media_proxy_linking(self, spacename, linkname):
        """Disable proxy linking on a space"""

        enc = base64.b64encode(linkname.encode())
        return self.delete("/v1/spaces/{}/media_proxies/{}".format(spacename, enc))

    def enable_media_proxy_linking(self, spacename):
        """Enable proxy linking on a space"""

        data = {"media_proxies": {"scheme": "efs_links", "path": ".flow_proxies"}}

        return self.put("/v1/spaces/{}".format(spacename), data)
