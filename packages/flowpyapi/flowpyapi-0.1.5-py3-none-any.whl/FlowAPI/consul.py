"""Helper for calling the Consul service REST api

https://www.consul.io/api-docs
"""
import json
import logging

import requests
from requests import Session

_logger = logging.getLogger(__name__)


class ConsulAPI:
    """A class to wrap Consul service REST API"""

    api_version = "v1"
    default_session = Session()

    def __init__(
        self,
        host="127.0.0.1",
        port=8500,
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

        full_url = "http://{}:{}/{}{}".format(
            self.host, self.port, self.api_version, endpoint
        )
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

    def get_service(self, service_name, only_passing=True):
        """Returns service health information"""

        url = "/health/service/{}".format(service_name)
        if only_passing:
            url += "?passing=true"
        return self.get(url)

    def get_service_ip(self, service_name):
        """Get the ip of a healthy node for the service specified"""

        health_data = self.get_service(service_name, True)
        if not health_data:
            return False
        if len(health_data) < 1:
            return False
        node = health_data[0]["Node"]
        return node["Address"]
