"""
Core classes and functions for FLOW (and other EditShare) api access
"""
import errno
import http.client
import json
import os
import socket
import ssl
import urllib
from base64 import b64encode

# Ports to connect on
ADMIN_PORT = 12104
AUTOMATION_PORT = 12141
METADATA_PORT = 12154
DAEMON_PORT = 12124
TRANSFER_PORT = 12194
INGEST_PORT = 12114
TRANSCODE_PORT = 12184
SCAN_PORT = 12134
SCANWORKER_PORT = 12334
SEARCH_PORT = 12304
SYNC_PORT = 12224
AUTOMATION_PORT = 12144
PROXYWORKER_PORT = 12164
RENDERMASTER_PORT = 12254

GATEWAY_PORT = 8006


def jprint(json_data):
    """Dump a json object"""
    print(json.dumps(json_data, indent=2))


def create_instance(api, host_ip, username, password):
    """Create and connect directly to service server"""

    service = api()
    service.connect(host_ip, username, password)
    return service


def create_gateway_instance_inner(api, username, password, ip_addr):
    """Create and connect to service via the local gateway"""

    if not ip_addr:
        ip_addr = os.environ.get("EDITSHARE_DOCKER_GATEWAY", "127.0.0.1")
    service = api()
    service.setUseGateway(True)
    service.connect2(ip_addr, GATEWAY_PORT, username, password)
    return service


class Connection:
    """A base class for wrapping endpoints of an EditShare REST API"""

    # pylint: disable=too-many-instance-attributes,too-many-public-methods

    def __init__(self):
        """Initialize instance attributes"""

        # print("Connection::__init__")
        self._conn = None
        # self._headers = None
        self._basic_auth_data = None
        self._username = None
        self._password = None
        self._port = None
        self._ip = None
        self._use_gateway = False
        self._last_return_code = 0
        self._last_headers = None
        self._content_type = None
        self._last_response = None
        self._service_name = None
        self._site_uuid = None
        self._node_uuid = None
        self._gateway_prefix = "/api/v2/"

    @staticmethod
    def bool_from_reply(func, reply):
        """Return a boolean value from json response"""

        # print( "bool_from_reply", reply )
        if len(reply) == 0:
            return False
        return_value = json.loads(reply)
        # print( "reply=", rv )
        if return_value != "OK":
            print(func + " failed:", return_value)
        return return_value == "OK"

    def connect3(self, host_ip, port):
        """
        Derived classes often override connect
        So we provide another version for external use
        """

        if self._use_gateway:
            port = GATEWAY_PORT
        self._conn = http.client.HTTPConnection(host_ip, port)
        self._ip = host_ip
        self._port = port

    def connect(self, host_ip, port):
        """Create a http connection"""

        if self._use_gateway:
            port = GATEWAY_PORT
        self._conn = http.client.HTTPConnection(host_ip, port)
        self._ip = host_ip
        self._port = port

    def connect2(self, host_ip, port, username, password):
        """Create a connection using https"""

        if self._use_gateway:
            port = GATEWAY_PORT

        # This sets up the https connection
        self._conn = http.client.HTTPSConnection(
            host_ip, port, context=ssl._create_unverified_context()
        )

        # we need to base 64 encode it
        # and then decode it to acsii as python 3 stores it as a byte string
        userpass = username + ":" + password
        user_and_pass = b64encode(userpass.encode()).decode()
        # self._headers = { 'Authorization' : 'Basic %s' %  userAndPass }
        self._basic_auth_data = "Basic %s" % user_and_pass
        self._username = username
        self._password = password
        self._ip = host_ip
        self._port = port

    def close(self):
        """Close our connection"""

        # print( "Connection close" )
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def reconnect(self):
        """Close our connection and connect again"""

        self.close()

        if self._basic_auth_data:
            self.connect2(self._ip, self._port, self._username, self._password)
        else:
            self.connect(self._ip, self._port)

    def do_request(self, verb, endpoint, data):
        """Make an HTTP request"""
        # pylint: disable=too-many-branches,too-many-statements

        if self._use_gateway:
            if endpoint.startswith("/" + self._service_name):
                endpoint = endpoint[len("/" + self._service_name) :]

            site_part = ""
            if self._site_uuid:
                site_part = self._site_uuid + "."
            node_part = ""
            if self._node_uuid:
                node_part = "." + self._node_uuid
            endpoint = (
                self._gateway_prefix
                + site_part
                + self._service_name
                + node_part
                + endpoint
            )

        debug_output = False

        if debug_output:
            print(
                "FlowAPI endpoint: https://{}:{}{}".format(
                    self._ip, self._port, endpoint
                )
            )
            self._conn.set_debuglevel(1)
            print(self._basic_auth_data)

        while True:
            self._conn.putrequest(verb, endpoint)

            if self._basic_auth_data:
                self._conn.putheader("Authorization", self._basic_auth_data)
            self._conn.putheader("X-Flow-Service", "flow-python-api")

            data_length = 0

            try:
                if data:
                    data_length = len(data)
                self._conn.putheader("Content-length", data_length)

                if self._content_type:
                    self._conn.putheader("Content-Type", self._content_type)

                self._conn.endheaders()

                if data:
                    # if data is bytes data read from a binary file,
                    # don't encode
                    if hasattr(data, "encode"):
                        self._conn.send(data.encode())
                    else:
                        self._conn.send(data)

                response = self._conn.getresponse()

                self._last_response = response.read().decode()
                self._last_return_code = response.status
                self._last_headers = response.getheaders()
                break

            except socket.error as exc:
                if exc.errno == errno.ETIMEDOUT:
                    self._last_response = (
                        "A connection attempt failed because the connected"
                        + " party did not properly respond after a period of time"
                    )
                    break

                if exc.errno == errno.ECONNREFUSED:
                    self._last_response = (
                        "No connection could be made because"
                        + " the target machine actively refused it"
                    )
                    break

                if exc.errno == 11001:
                    self._last_response = "getaddrinfo failed"
                    break

                if exc.errno == 10065:
                    self._last_response = (
                        "A socket operation was attempted to an unreachable host"
                    )
                    break

                print(
                    "socket.error exception! '{}' errno: {}. Retrying...".format(
                        exc, exc.errno
                    )
                )

                if "[SSL: UNKNOWN_PROTOCOL]" in str(exc):
                    self._last_response = "SSL: Unknown Protocol"
                    break

                if "[SSL: WRONG_VERSION_NUMBER]" in str(exc):
                    self._last_response = "SSL: Unknown Protocol"
                    break

                self.reconnect()

            except http.client.CannotSendRequest as exc:
                print("CannotSendRequest exception! {}".format(exc))
                break

            except http.client.BadStatusLine:
                # we can hit this if the connection is closed
                # we need to reconnect in that case
                print("BadStatusLine exception! '{}'".format(endpoint))
                self.reconnect()

        if debug_output:
            print(self._last_return_code)
            print(self._last_headers)
            print(self._last_response)

        return self._last_response

    def get(self, path):
        """Do an HTTP GET request"""

        return self.do_request("GET", path, "")

    def post(self, path, data):
        """Do an HTTP POST request"""

        if isinstance(data, dict):
            data = json.dumps(data)
        return self.do_request("POST", path, data)

    def put(self, path, data=""):
        """Do an HTTP PUT request"""

        if isinstance(data, dict):
            data = json.dumps(data)
        return self.do_request("PUT", path, data)

    def patch(self, path, data=""):
        """Do an HTTP PATCH request"""

        if isinstance(data, dict):
            data = json.dumps(data)
        return self.do_request("PATCH", path, data)

    def delete(self, path, data=""):
        """Do an HTTP DELETE request"""

        if isinstance(data, dict):
            data = json.dumps(data)
        return self.do_request("DELETE", path, data)

    def lastReturnCode(self):
        """Return last HTTP return code"""

        return int(self._last_return_code)

    def lastReturnHeaders(self):
        """Return last HTTP returned headers"""

        return self._last_headers

    def lastResponse(self):
        """Return last HTTP returned response body"""

        return self._last_response

    def setUseGateway(self, enable):
        """Enable using the gateway"""

        self._use_gateway = enable

    def setSite(self, site_uuid):
        """Enable using a specific site"""

        self._site_uuid = site_uuid

    def setNode(self, node_uuid):
        """Enable using a specific node"""

        self._node_uuid = node_uuid

    def version(self):
        """Call the common version endpoint"""

        return self.get("/version")

    def deleteThatReturnsBOOL(self, ident, endpoint):
        """Return boolean result from a HTTP DELETE request"""

        reply = self.delete(endpoint)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply(ident, reply)

    def postThatReturnsID(self, endpoint, data):
        """Return the 'id' (usually a database id) from a post request"""

        reply = self.post(endpoint, json.dumps(data))
        if self.lastReturnCode() != 200 and self.lastReturnCode() != 201:
            return False
        return int(reply)

    def postThatReturnsObj(self, endpoint, data):
        """Return the dictionary returned from a POST request"""

        if data:
            reply = self.post(endpoint, json.dumps(data))
        else:
            reply = self.post(endpoint, None)
        if self.lastReturnCode() != 200 and self.lastReturnCode() != 201:
            return False
        obj = json.loads(reply)
        return obj

    def postThatReturnsBOOL(self, endpoint, data):
        """Return true if 'ok' response"""

        if data:
            reply = self.post(endpoint, json.dumps(data))
        else:
            reply = self.post(endpoint, None)
        if self.lastReturnCode() != 200 and self.lastReturnCode() != 201:
            return False
        return self.bool_from_reply("postThatReturnsBOOL", reply)

    def getThatReturnsObj(self, endpoint):
        """Return the dictionary returned from a GET request"""

        reply = self.get(endpoint)
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        return obj

    def putThatReturnsBOOL(self, ident, endpoint, data):
        """Return boolean result from a HTTP PUT request"""

        reply = self.put(endpoint, json.dumps(data))
        # print( reply )
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply(ident, reply)

    def patch_to_bool(self, ident, endpoint, data):
        """Return boolean result from a HTTP PATCH request"""

        reply = self.patch(endpoint, json.dumps(data))
        # print( reply )
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply(ident, reply)

    def ping(self):
        """Call the common ping endpoint"""

        return self.getThatReturnsObj("/ping")

    @staticmethod
    def safe_url_string(input_s):
        """Escape a string for safe use in an endpoint"""

        return str(urllib.parse.quote(str(input_s)))
