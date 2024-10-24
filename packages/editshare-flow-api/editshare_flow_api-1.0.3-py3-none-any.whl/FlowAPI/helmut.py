"""Helper for calling Helmut REST api

http://repo.moovit24.de:8889
"""
import json
import logging
import urllib.parse
from typing import List, Optional

import requests
from requests import Session

# from .core import jprint

_logger = logging.getLogger(__name__)

HELMUT_PORT = 8014


class HelmutAPI:
    """A base class for Helmut api usage"""

    api_version = "v1"
    default_session = Session()

    def __init__(
        self,
        host: str,
        token: str,
        service_name: str,
        port: int,
    ) -> None:
        """Construct the object"""
        self.host = host
        self.token = token
        self.service_name = ""
        if service_name:
            self.service_name = "/" + service_name
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

    def put(self, endpoint, data=None, query_params=None):
        """Put request"""

        response = self._request("PUT", endpoint, data, query_params)
        return response.status_code == 200

    def delete(self, endpoint, data=None, query_params=None):
        """Delete request"""

        response = self._request("DELETE", endpoint, data, query_params)
        return response.status_code == 200

    def post(self, endpoint, data=None, query_params=None):
        """POST request"""

        response = self._request("POST", endpoint, data, query_params)
        if response.status_code in (200, 201):
            return json.loads(response.content)

        return False

    def _request(self, verb, endpoint, data=None, query_params=None):
        """Run an http request"""

        ssl_connection = self.port == 443
        http_prefix = "https" if ssl_connection else "http"

        full_url = "{}://{}:{}/{}{}{}".format(
            http_prefix,
            self.host,
            self.port,
            self.api_version,
            self.service_name,
            endpoint,
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.token:
            headers["Authorization"] = "Bearer " + self.token

        response = None
        # _logger.debug("%s %s", verb, full_url)

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

        # _logger.debug(
        #     "HTTP Response Code: %s, Body: %s",
        #     response.status_code,
        #     response.text,
        # )

        if response.status_code < 200 or response.status_code > 299:
            _logger.error("%s %s failed %d", verb, full_url, response.status_code)
            # return False
        # _logger.debug(response.status_code)
        # _logger.debug(response.headers)
        # data = json.loads(response.content)
        # return data
        return response


class StreamsAPI(HelmutAPI):
    """A class to wrap the Helmut streams apis"""

    @staticmethod
    def create(
        host: str,
        token: str,
        *,
        port=HELMUT_PORT,
    ) -> object:
        """Create an instance of the StreamsAPI"""
        return StreamsAPI(host=host, token=token, service_name="streams", port=port)

    def get_all_variables(self):
        """Get a list of all variables"""

        return self.get("/store")

    def update_variable(self, data):
        """Update an existing variable in the store"""

        escaped_name = urllib.parse.quote(str(data["key"]))
        return self.put("/store/{}?isNode=False".format(escaped_name), data)

    def delete_variable(self, key):
        """Delete an existing variable in the store"""

        escaped_name = urllib.parse.quote(key)
        params = {"isNode": False}
        return self.delete("/store/{}".format(escaped_name), None, params)

    def create_variable(self, data):
        """Create a new variable in the store"""

        return self.post("/store", data)

    def get_variable(self, key):
        """Get a specific variable"""

        escaped_name = urllib.parse.quote(str(key))
        return self.get("/store/" + escaped_name)

    def version(self):
        """Service version"""
        return self.get("/version")


class IoAPI(HelmutAPI):
    """A class to wrap the Helmut IO apis"""

    @staticmethod
    def create(
        host: str,
        token: str,
        *,
        port=HELMUT_PORT,
    ) -> object:
        """Create an instance of the IoAPI"""
        return IoAPI(host=host, token=token, service_name="io", port=port)

    def version(self):
        """Service version"""
        return self.get("/version")

    def get_all_jobs(self, start=0, count=100):
        """Get all jobs"""
        return self.get("/jobs?page={}&limit={}".format(start, count))

    def get_job(self, job_id):
        """Get a job"""
        return self.get("/jobs/" + job_id)

    def create_job(self, job_data):
        """Create a job"""
        return self.post("/jobs", job_data)

    def get_all_profiles(self):
        """Get all profiles"""
        return self.get("/profile/all")

    def find_profile(self, profile_name):
        """Find a profile with a given name"""
        profiles = self.get_all_profiles()
        for profile in profiles:
            if profile["name"] == profile_name:
                return profile
        return False


class PreferencesAPI(HelmutAPI):
    """A class to wrap the Helmut Preferences apis"""

    @staticmethod
    def create(
        host: str,
        token: str,
        *,
        port=HELMUT_PORT,
    ) -> object:
        """Create an instance of PreferencesAPI"""
        return PreferencesAPI(
            host=host, token=token, service_name="preferences", port=port
        )

    def version(self):
        """Service version"""

        return self.get("/version")

    def get_all(self):
        """Get all preferences"""

        return self.get("")

    def update(self, pref_data):
        """Update a preference
        Note - it is important to include all the data here
        as the whole thing is replaced by what we send
        """

        return self.put("", pref_data)

    def update_key_value(self, key_name, value_data):
        """Helper to update the value of the given key"""

        pref = self.find_by_key(key_name)
        if pref:
            pref["value"] = value_data
            return self.update(pref)
        return False

    def find_by_key(self, key_name):
        """Find a preference from a key name"""

        prefs = self.get_all()
        for pref in prefs:
            if pref["key"] == key_name:
                return pref
        return {}


class FxAPI(HelmutAPI):
    """A class to wrap the Helmut FX apis"""

    @staticmethod
    def create(
        host: str,
        token: str,
        *,
        port=HELMUT_PORT,
    ) -> object:
        """Create an instance of FxAPI"""
        return FxAPI(host=host, token=token, service_name="fx", port=port)

    def version(self):
        """Service version"""
        return self.get("/version")

    def all_projects(self):
        """Get a list of all projects"""

        search_data = {"any": False, "filter": []}
        return self.post("/projects/search", search_data)

    def get_project(self, project_id):
        """Get a projects"""
        return self.get("/projects/{}".format(project_id))

    def delete_project(self, project_id):
        """Delete a project"""
        return self.delete("/projects/{}".format(project_id))

    def find_project(self, project_name):
        """Search for projects"""

        # example:
        # {"any":false,"filter":[{"key":"group","comparator":"IS","value":"All"},
        # {"key":"category","comparator":"IS","value":"All"},
        # {"key":"template","comparator":"IS","value":"All"}]}
        search_data = {
            "any": False,
            "filter": [{"key": "name", "comparator": "IS", "value": project_name}],
        }
        response = self.post("/projects/search", search_data)
        if not response:
            return None
        return response[0]

    def get_group_categories(self, group_name):
        """Get categories for a group"""

        return self.get("/templates/{}".format(urllib.parse.quote(group_name)))

    def create_group_category(self, group_name, category_name):
        """Create a new group in a category"""

        url = "/templates/" + urllib.parse.quote(group_name)
        url += "/" + urllib.parse.quote(category_name)
        return self.post(url)

    def ensure_group_category(self, group_name, category_name):
        """Create a new group in a category"""

        existing_categories = self.get_group_categories(group_name)
        if category_name in existing_categories:
            return {"name": category_name}
        return self.create_group_category(group_name, category_name)


class UsersAPI(HelmutAPI):
    """A class to wrap the Helmut Users apis"""

    @staticmethod
    def create(
        host: str,
        token: str = "",
        port=HELMUT_PORT,
    ) -> object:
        """Create an instance of UsersAPI"""
        return UsersAPI(host=host, token=token, service_name="members", port=port)

    def version(self):
        """Service version"""
        return self.get("/version")

    def login(self, username, password):
        """Login and return a bearer token"""

        escaped_username = urllib.parse.quote(username)
        escaped_password = urllib.parse.quote(password)
        token_backup = self.token
        self.token = None
        auth_object = self.post(
            "/auth/login?username={}&password={}&responseWithToken=true".format(
                escaped_username, escaped_password
            ),
            None,
        )
        self.token = token_backup
        if not auth_object:
            return False
        if "token" in auth_object:
            self.token = auth_object["token"]
            return auth_object["token"]
        return False

    def get_all_groups(self):
        """Get a list of all groups"""

        return self.get("/groups")

    def find_group(self, group_name):
        """Find a group by name"""

        escaped_group_name = urllib.parse.quote(group_name)
        return self.get("/groups/name/{}".format(escaped_group_name))

    def create_group(self, group_name):
        """Create a new group.

        :returns: The group object
        """

        group_data = {"name": group_name}
        return self.post("/groups", group_data)

    def ensure_group(self, group_name):
        """Ensure a group exists.

        :returns: The group object
        """

        group_data = self.find_group(group_name)
        if group_data:
            return group_data
        return self.create_group(group_name)

    def get_users(self, group_id="All"):
        """Get a list of all users"""

        return self.get("/users/search?groupFilter={}".format(group_id))

    def add_user_to_group(self, user_id, group_id):
        """Add a user to a group"""

        payload = {"userId": user_id, "groupId": group_id}

        return self.put("/users/group/add", payload)


class MetadataAPI(HelmutAPI):
    """A class to wrap the Helmut Metadata apis"""

    @staticmethod
    def create(
        host: str,
        token: str,
        *,
        port=HELMUT_PORT,
    ) -> object:
        """Create an instance of MetadataAPI"""
        return MetadataAPI(host=host, token=token, service_name="", port=port)

    def version(self):
        """Service version"""
        return self.get("/metadata/version")

    def get_all(self):
        """Get all metadata fields"""
        return self.get("/metadata")

    def get_by_name(self, metadata_field_name):
        """Helper to get a metadata field by name"""

        all_fields = self.get_all()

        for field in all_fields:
            if field["name"] == metadata_field_name:
                return field

        return {}

    def create_field(self, data):
        """Create a new metadata field"""

        return self.post("/metadata", data)

    def get_all_sets(self):
        """Get all metadata sets"""
        return self.get("/metadataSet")

    def update_field(self, data):
        """Update an existing metadata field"""

        return self.put("/metadata", data)


class CosmoAPI(HelmutAPI):
    """A class to wrap the Helmut Cosmo apis"""

    @staticmethod
    def create(
        host: str,
        token: str,
        *,
        port=HELMUT_PORT,
    ) -> object:
        """Create an instance of CosmoAPI"""
        return CosmoAPI(host=host, token=token, service_name="co", port=port)

    def get_project_assets(self, project_id):
        """Get all assets in a project"""

        return self.get("/assets/" + project_id)

    def find_assets_by_path(
        self, file_path: str, project_id: Optional[str] = None
    ) -> List:
        # pylint: disable=line-too-long
        """Find an asset in a project by mediaspace + path
        Example would be:
        /Volumes/AS-2023-02-14-A_1/Media/Footage_Original/01_From_Archive/c2023-02-14-10-45-12-01.mxf

        returns a list
        """

        all_assets = self.post("/assets/getByPath", file_path)
        if not all_assets:
            return all_assets
        if not project_id:
            return all_assets

        return_assets = []

        for asset in all_assets:
            if "projectId" in asset and asset["projectId"] == project_id:
                return_assets.append(asset)
        return return_assets

    def get_asset(self, asset_id, os_type="AUTO"):
        """Get an asset by its id"""

        url = "/assets?assetId={}&os={}".format(asset_id, os_type)
        return self.get(url)

    def attach_proxy(self, project_id, asset_id, high_res_path, proxy_path):
        """Attach a proxy"""

        proxy_data = {
            "highresPath": high_res_path,
            "proxyPath": proxy_path,
            "projectId": project_id,
        }

        url = "/assets/proxy?os=UNIX&assetId={}".format(asset_id)
        return self.post(url, proxy_data)

    def create_asset(self, asset_data):
        """Adds a new asset"""

        return self.post("/assets", asset_data)

    def delete_asset(self, asset_id):
        """Delete an asset"""

        return self.delete("/assets?assetId=" + asset_id)

    def version(self):
        """Service version"""
        return self.get("/version")
