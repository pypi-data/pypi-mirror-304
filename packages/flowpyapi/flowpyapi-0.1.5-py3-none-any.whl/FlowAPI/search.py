"""
FLOW Search service API
See here: https://developers.editshare.com
"""
import json
import time

from .core import (
    SEARCH_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)


class Search(Connection):
    """Wraps the search service api"""

    # pylint: disable=consider-using-f-string

    def __init__(self):
        super().__init__()
        self._service_name = "search"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Search, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr="127.0.0.1"):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Search, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        return Connection.connect2(self, ip_addr, SEARCH_PORT, username, password)

    def find_clips_in_space(self, space_name):

        """Helper to find all clips in a mediaspace"""

        data = {
            "combine": "MATCH_ALL",
            "filters": [
                {
                    "field": {
                        "fixed_field": "MEDIA_SPACES_NAMES",
                        "group": "SEARCH_NONE",
                        "type": "QString",
                    },
                    "match": "EQUAL_TO",
                    "search": space_name,
                }
            ],
        }

        search_results = self.doSearch(data)

        # print( len(searchResults))
        rv_list = []
        for i in search_results:
            if "clip_id" in i:
                rv_list.append(int(i["clip_id"]))

        return rv_list

    def findClipByName(self, name):

        """Helper to find all clips with matching name"""
        data = {
            "combine": "MATCH_ANY",
            "filters": [
                {
                    "field": {
                        "fixed_field": "CLIPNAME",
                        "group": "SEARCH_FILES",
                        "type": "QString",
                    },
                    "match": "CONTAINS",
                    "search": name,
                }
            ],
        }

        search_results = self.doSearch(data)

        # print( len(searchResults))
        rv_list = []
        for i in search_results:
            if "clip_id" in i:
                rv_list.append(int(i["clip_id"]))

        return rv_list

    # Wrap the /search/cached endpoint
    def createSearch(self, search_string):
        url = "/search/cached?" + search_string
        reply = self.post(url, "")
        if not reply:
            return False
        return json.loads(reply)

    # do a synchronous search
    def doSearch(self, data):
        return self.postThatReturnsObj("/search", data)

    # get results from a cached search
    def searchResults(self, search_id, start=0, end=100):
        our_id = search_id
        if "cache_id" in search_id:
            our_id = search_id["cache_id"]
        url = "/search/cached/{}?start={}&max_results={}".format(our_id, start, end)
        return self.getThatReturnsObj(url)

    def waitForSearch(self, search_id):
        our_id = search_id
        if "cache_id" in search_id:
            our_id = search_id["cache_id"]
        while True:
            res = self.searchResults(our_id, 0, 1)
            if not res:
                return False
            if res["complete"]:
                return True
            time.sleep(0.5)

    def deleteSearch(self, search_id):
        our_id = search_id
        if "cache_id" in search_id:
            our_id = search_id["cache_id"]
        reply = self.delete("/search/cached/" + str(our_id))
        return self.bool_from_reply("deleteSearch", reply)

    # Find and return first sequence with name
    def findSequence(self, sequence_name):
        reply = self.get("/search?q=" + sequence_name + "&sequences=true")
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        for i in obj:
            if "sequence_id" in i:
                return int(i["sequence_id"])
        return False
