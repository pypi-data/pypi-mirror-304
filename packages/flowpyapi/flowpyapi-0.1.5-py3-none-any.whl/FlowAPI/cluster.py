"""Helper for calling the EditShare Cluster REST api

note sure if there are any docs
"""
import json
import logging

import requests
import urllib3
from requests import Session

from .consul import ConsulAPI

_logger = logging.getLogger(__name__)


class ClusterAPI:
    """A class to wrap EditShare Cluster service REST API"""

    default_session = Session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(
        self,
        host="127.0.0.1",
        port=8085,
    ) -> None:
        """Construct the object"""
        self.host = host
        self.port = port

    def get_session(self):
        """Return default for now"""

        return self.default_session

    def get(self, endpoint, data=None, query_params=None):
        """Get request"""

        response = self._request("GET", endpoint, data, query_params)
        if response.status_code != 200:
            return False
        data = json.loads(response.content)
        return data

    def _request(self, verb, endpoint, data=None, query_params=None):
        """Run an http request"""

        full_url = "https://{}:{}{}".format(self.host, self.port, endpoint)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = None
        _logger.debug("HTTP %s %s", verb, full_url)

        try:
            response = self.get_session().request(
                verb,
                full_url,
                json=data,
                params=query_params,
                headers=headers,
                verify=False,
            )
        except requests.exceptions.ConnectionError as err:
            _logger.error("Exception sending to Helmut")
            raise err

        _logger.debug(
            "HTTP Response Code: %s, Body: %s",
            response.status_code,
            response.text,
        )

        if response.status_code < 200 or response.status_code > 299:
            _logger.error("GET %s failed %d", full_url, response.status_code)
            # return False
        # _logger.debug(response.status_code)
        # _logger.debug(response.headers)
        # data = json.loads(response.content)
        # return data
        return response

    def get_stacks(self):
        """Returns stacks information"""

        return self.get("/stacks")

    def get_hosts(self):
        """Returns hosts information"""

        return self.get("/cluster/hosts")

    def get_self(self):
        """Returns self information"""

        return self.get("/cluster/hosts/_self")

    def get_storage_ha_vip(self):
        """Get the virtual ip of storage HA stack
        (not the EFS HA stack)
        """

        # In a non HA system this will return nothing
        stacks = self.get_stacks()
        storage_ip = None

        if stacks:
            for stack in stacks:
                if stack["type"] == "storage-master":
                    storage_ip = stack["ip"]
                    break

        # Fall back to consul
        if not storage_ip:
            consul_api = ConsulAPI(self.host)
            storage_ip = consul_api.get_service_ip("esa")

        return storage_ip
