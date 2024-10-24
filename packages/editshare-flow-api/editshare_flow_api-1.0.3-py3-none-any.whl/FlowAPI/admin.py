"""
FLOW Admin service API
See here: https://developers.editshare.com/?urls.primaryName=EditShare%20FLOW%20Admin
"""
import json
import logging
import platform
import socket
import time
from typing import Any, Dict, List

from .core import ADMIN_PORT, Connection, create_gateway_instance_inner, create_instance
from .editshare import EditShare

FlowObject = Dict[Any, Any]


class Admin(Connection):
    """Wraps the admin server api"""

    # pylint: disable=too-many-public-methods

    def __init__(self):
        super().__init__()
        self._service_name = "admin"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Admin, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Admin, username, password, ip_addr)

    def connect(self, ip, username, password):
        """Connect to admin server"""

        return Connection.connect2(self, ip, ADMIN_PORT, username, password)

    def login(self, user, app):
        """Login to the system"""

        reply = self.put("/login/" + user, app)
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        return obj

    def logout(self, user):
        """Log out from the system"""

        reply = self.put("/login/" + user)
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        return obj

    def getServiceDetails(self, name):
        """Get information about a service"""

        return self.getThatReturnsObj("/service-details/" + name)

    def getServicesStatus(self):
        """Get service status"""

        return self.getThatReturnsObj("/service/status")

    def createDatabaseBackupJob(self):
        """Create a database backup job"""

        return self.postThatReturnsObj("/configuration/database/backup/job", "")

    def getDatabaseBackupJob(self, job_id):
        """Fetch a database backup job"""

        return self.getThatReturnsObj("/configuration/database/backup/job/" + job_id)

    def deleteDatabaseBackupJob(self, job_id):
        """Delete a database backup job"""

        reply = self.delete("/configuration/database/backup/job/" + job_id)
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("deleteDatabaseBackupJob", reply)

    def getMediaspaces(self):
        """Get a list of all spaces"""

        return self.get_mediaspaces(False)

    def get_mediaspaces(self, as_admin=False):
        """Get a list of all spaces"""

        url = "/mediaspaces"
        if as_admin:
            url += "?admin=true"
        return self.getThatReturnsObj(url)

    def createTestMountJob(self, mountpoint_id):
        """Create a mounting test job"""

        return self.postThatReturnsObj("/mount/test/" + str(mountpoint_id), None)

    def getTestMountJob(self, job_id):
        """Fetch a mounting test job"""

        return self.getThatReturnsObj("/mount/test/" + job_id)

    def getClusterDetails(self):
        """Get cluster information"""

        return self.getThatReturnsObj("/cluster")

    def getMediaspace(self, name):
        """Get a mediaspace by name"""

        url = "/mediaspaces?name=" + self.safe_url_string(name)
        return self.getThatReturnsObj(url)

    def getMediaspaceAsAdmin(self, name):
        """Get a mediaspace by name"""

        url = "/mediaspaces?name=" + self.safe_url_string(name) + "&admin=true"
        return self.getThatReturnsObj(url)

    def find_mediaspace(self, spacename, as_admin=False):
        """Find a mediaspace by name"""

        escaped_name = self.safe_url_string(spacename)
        url = "/mediaspaces?name=" + escaped_name
        if as_admin:
            url += "&admin=true"
        return self.getThatReturnsObj(url)

    def find_mediaspace_on_site(self, site_uuid, spacename, as_admin=False):
        """Find a mediaspace by name on a site"""

        # Cannot currently filter by site so we need to fetch them all
        all_spaces = self.get_mediaspaces(as_admin)

        for space in all_spaces:
            if space["name"] == spacename and space["site"]["uuid"] == site_uuid:
                return space

        return FlowObject()

    def getMediaspaceByID(self, mediaspace_id, as_admin=False):
        """Get a mediaspace by (uu)id"""

        url = "/mediaspaces/" + str(mediaspace_id)
        if as_admin:
            url += "?admin=true"
        return self.getThatReturnsObj(url)

    def createMediaspace(self, data):
        """Create a new mediaspace"""

        return self.postThatReturnsID("/mediaspaces", data)

    def getMediaspaceDefaultDirectory(self, mediaspace_id, wrapper="unknown"):
        """Get the default capture/ingest directory for a mediaspace, wrapper combo"""

        url = (
            "/mediaspaces/"
            + str(mediaspace_id)
            + "/defaultDir?hostname="
            + socket.gethostname()
            + "&os="
            + platform.system()
            + "&wrapper="
            + wrapper
        )
        # print( url )
        return self.getThatReturnsObj(url)

    def getSpaceUsers(self, mediaspace_id):
        """Get all the users who are members of the space"""

        url = "/mediaspaces/" + str(mediaspace_id) + "/users"
        # print( url )
        return self.getThatReturnsObj(url)

    def linkUsersToSpace(self, mediaspace_id, data):
        """Add users to a space"""

        return self.putThatReturnsBOOL(
            "linkUsersToSpace", "/mediaspaces/{}/users/add".format(mediaspace_id), data
        )

    def unlinkUsersFromSpace(self, mediaspace_id, data):
        """Remove users from a space"""

        return self.putThatReturnsBOOL(
            "linkUsersToSpace",
            "/mediaspaces/{}/users/remove".format(mediaspace_id),
            data,
        )

    def getMediaspaceFolders(self, mediaspace_id, path=""):
        """Get mediaspace folders"""

        url = "/mediaspaces/{}/folders".format(mediaspace_id)
        if path:
            escaped_path = self.safe_url_string(path)
            url += "/" + escaped_path
        if True:
            url += "?database=false"
        return self.getThatReturnsObj(url)

    def makeMediaspacePath(self, mediaspace_id: int, path: str) -> bool:
        """Create mediaspace folder"""

        escaped_path = self.safe_url_string(path)
        return self.putThatReturnsBOOL(
            "getMediaspacePath",
            "/mediaspaces/{}/folders/{}".format(mediaspace_id, escaped_path),
            "",
        )

    def deleteMediaspace(self, ms_id, from_database=False):
        """Remove a mediaspace"""

        url = "/mediaspaces/" + str(ms_id)
        if from_database:
            url += "?from_database=true"
        return self.deleteThatReturnsBOOL("deleteMediaspace", url)

    def mountpoints(self, as_admin=False):
        """Get all mount points for connecting user or all if user is admin and as_admin is True"""

        url = "/mountpoints"
        if as_admin:
            url += "?admin=true"
        return self.getThatReturnsObj(url)

    def mountpointByID(self, mountpoint_id):
        """Get mount point with matching (uu)id"""

        url = "/mountpoints/" + str(mountpoint_id)
        return self.getThatReturnsObj(url)

    def mountpointByName(self, name):
        """Get mountpoint with matching name"""

        url = "/mountpoints?name=" + self.safe_url_string(name)
        return self.getThatReturnsObj(url)

    def userList(self):
        """Get a list of all the users"""
        return self.getThatReturnsObj("/users")

    def getUser(self, user_id):
        """Get a specific user"""

        return self.getThatReturnsObj("/users/" + str(user_id))

    def findUser(self, user_name: str) -> FlowObject:
        """Find a new user by name"""

        return self.getThatReturnsObj("/users?username=" + str(user_name))

    def create_user(self, user: object) -> FlowObject:
        """Create a new user"""

        return self.postThatReturnsObj("/users", user)

    def createUser(self, user: object) -> FlowObject:
        """Create a new user"""

        return self.create_user(user)

    def updateUser(self, user: dict):
        """Update a user's details"""

        return self.putThatReturnsBOOL(
            "updateUser", "/users/" + str(user["user_id"]), user
        )

    def deleteUser(self, user):
        """Remove a user"""

        return self.deleteThatReturnsBOOL(
            "deleteUser", "/users/" + str(user["user_id"])
        )

    def ensure_user_exists(self, user_data: FlowObject) -> FlowObject:
        """If user does not exist, create them"""

        rv_obj = self.findUser(user_data["username"])
        if not rv_obj:
            if self.lastReturnCode() != 404:
                return FlowObject()

            rv_obj = self.createUser(user_data)
        return rv_obj

    def ensureUserExists(
        self,
        username: str,
        password: str,
        applications: List = None,
        features: List = None,
    ) -> FlowObject:
        """If user does not exist, create them"""

        user_data = {
            "username": username,
            "password": password,
            "applications": applications,
            "features": features,
        }
        return self.ensure_user_exists(user_data)

    def ensure_space_exists_on_site(
        self,
        site_uuid: str,
        spacename: str,
        spacetype: str,
        esa_ip: str = None,
    ) -> FlowObject:
        """Create EditShare space if necessary"""

        rv_obj = self.find_mediaspace_on_site(site_uuid, spacename, True)
        if rv_obj:
            return rv_obj

        if self.lastReturnCode() != 200:
            return FlowObject()

        logging.debug(
            "Need to create media space '%s' on site %s", spacename, site_uuid
        )
        storage_api = EditShare.create_gateway_instance(
            self._username, self._password, esa_ip
        )
        storage_api.setSite(site_uuid)
        bit_buckets = storage_api.get_bit_buckets()

        if not bit_buckets:
            logging.error(
                "ensure_space_exists_on_site: No bit buckets. site: %s Error Code: %d %s",
                site_uuid,
                storage_api.lastReturnCode(),
                storage_api.lastResponse(),
            )
            return FlowObject()

        new_space_data = {
            "name": spacename,
            "mount_type": "editshare",
            "project_type": spacetype,
            "credentials": {
                "bitbucket": {
                    "bucket": bit_buckets[0],
                    "site": {"uuid": site_uuid},
                },
                "structure_type": spacetype,
            },
        }

        # jprint(new_space_data)

        self.createMediaspace(new_space_data)

        # should be 201 and return the id of the new space
        if self.lastReturnCode() != 201:
            logging.error(
                "ensure_space_exists_on_site: Failed to create mediaspace. Error Code: %d %s",
                self.lastReturnCode(),
                self.lastResponse(),
            )
            return FlowObject()

        start = time.time()
        timeout_secs = 30

        while True:
            rv_obj = self.find_mediaspace_on_site(site_uuid, spacename, True)
            if rv_obj:
                break
            time.sleep(2)

            if time.time() - start > timeout_secs:
                return FlowObject()

        return rv_obj

    def ensureSpaceExists(
        self, spacename: str, spacetype: str, esa_ip: str = None
    ) -> FlowObject:
        """Create EditShare space if necessary"""

        rv_obj = self.getMediaspaceAsAdmin(spacename)
        if rv_obj:
            return rv_obj

        if self.lastReturnCode() != 404:
            return FlowObject()

        logging.debug("Need to create media space %s", spacename)

        if not esa_ip:
            sd = self.getServiceDetails("esa")
            esa_ip = sd["address"]
        esa = EditShare()
        esa.connect(esa_ip, self._username, self._password)
        bit_buckets = esa.get_bit_buckets()

        if not bit_buckets:
            logging.error(
                "ensureSpaceExists: No bit buckets. ip: %s Error Code: %d",
                sd["address"],
                esa.lastReturnCode(),
            )
            return FlowObject()

        new_space_data = {
            "name": spacename,
            "mount_type": "editshare",
            "project_type": spacetype,
            "credentials": {
                "bitbucket": bit_buckets[0],
                "structure_type": spacetype,
            },
        }

        self.createMediaspace(new_space_data)

        # print("createMediaspace")
        # print(ms)

        if self.lastReturnCode() != 201:
            print("Failed to create mediaspace")
            print(self.lastReturnCode())
            print(self.lastResponse())
            return FlowObject()

        # should be 201 and return the id of the new space

        start = time.time()
        timeout_secs = 30

        while True:
            rv_obj = self.getMediaspaceAsAdmin(spacename)
            if rv_obj:
                break
            time.sleep(2)

            if time.time() - start > timeout_secs:
                return FlowObject()

        return rv_obj

    def ensureUserIsInSpace(
        self, username: str, spacename: str, spacetype: str
    ) -> bool:
        """create space and add user if necessary
        User must already exist
        """
        space_obj = self.ensureSpaceExists(spacename, spacetype)
        if not space_obj:
            return False

        if space_obj["is_public"]:
            return True

        if self.is_user_in_space(space_obj["mediaspace_id"], username):
            return True

        if not self.linkUsersToSpace(space_obj["mediaspace_id"], [username]):
            return False

        return self.is_user_in_space(space_obj["mediaspace_id"], username)

    def get_space_groups(self, mediaspace_id) -> List:
        """Get user groups in a space"""

        url = "/mediaspaces/" + str(mediaspace_id) + "/groups?admin=true&groups=true"
        rv = self.getThatReturnsObj(url)
        if not rv:
            return []
        return rv["groups"]

    def link_groups_to_space(self, mediaspace_id: int, groupnames: List) -> bool:
        """Link a group to space membership"""

        group_list = self.get_space_groups(mediaspace_id)
        start_len = len(group_list)

        for newgroup in groupnames:
            found = False
            for group in group_list:
                if group["groupname"] == newgroup:
                    found = True
                    break
            if not found:
                # logging.debug("link_groups_to_space: group '%s' needs adding", newgroup)
                group_list.append({"access": True, "groupname": newgroup})

        if len(group_list) == start_len:
            return True
        # logging.debug(group_list)
        return self.putThatReturnsBOOL(
            "link_group_to_space",
            "/mediaspaces/{}/groups".format(mediaspace_id),
            group_list,
        )

    def get_user_group(self, group_name: str) -> FlowObject:
        """Get a user group"""

        url = "/groups/" + self.safe_url_string(group_name)
        return self.getThatReturnsObj(url)

    def create_user_group(self, group_data: FlowObject) -> FlowObject:
        """Create a new group"""

        # It seems that you cannot specify much when creating a user group
        # You have to update it afterwards in a specific way
        # We iron this stuff out here
        groupname = group_data["groupname"]
        data = {
            "groupname": groupname,
        }

        if "description" in group_data:
            data["description"] = group_data["description"]

        new_data = self.postThatReturnsObj("/groups", group_data)
        if not new_data:
            return new_data

        # Now update it
        data = {
            "groupname": groupname,
        }

        if "is_administrator" in group_data:
            data["is_administrator"] = group_data["is_administrator"]
        if "is_enabled" in group_data:
            data["is_enabled"] = group_data["is_enabled"]
        if "features" in group_data:
            data["features"] = group_data["features"]
        if "applications" in group_data:
            data["applications"] = group_data["applications"]

        if not self.update_user_group(data):
            return FlowObject()

        return self.get_user_group(groupname)

    def remove_user_group(self, group_name: str) -> bool:
        """Delete a user group"""

        url = "/groups/" + self.safe_url_string(group_name)
        return self.deleteThatReturnsBOOL("remove_user_group", url)

    def update_user_group(self, group_data: FlowObject) -> FlowObject:
        """Update a user group"""

        url = "/groups/" + self.safe_url_string(group_data["groupname"])
        return self.putThatReturnsBOOL("update_user_group", url, group_data)

    def get_group_users(self, group_name: str) -> List[str]:
        """Get a list of users in a group"""

        url = "/groups/" + self.safe_url_string(group_name) + "/users"
        response = self.getThatReturnsObj(url)
        if not response:
            response = []
        return response

    def get_user_groups(self) -> List[str]:
        """Get the list of user groups"""

        url = "/groups"
        response = self.getThatReturnsObj(url)
        if not response:
            response = []
        return response

    def add_users_to_group(self, group_name: str, users_to_add: List[str]) -> bool:
        """Add users to a group"""

        if not users_to_add:
            return True
        url = "/groups/" + self.safe_url_string(group_name) + "/users"
        return self.postThatReturnsBOOL(url, users_to_add)

    def ensure_users_in_group(self, group_name, user_list):
        """Add users who are not in a group"""

        existing_users = self.get_group_users(group_name)
        if not existing_users:
            existing_users = []

        users_to_add = []
        for user in user_list:
            if user not in existing_users:
                users_to_add.append(user)
                logging.debug("Adding '%s' to group '%s'", user, group_name)

        return self.add_users_to_group(group_name, users_to_add)

    def is_user_in_space(self, mediaspace_id, username) -> bool:
        """Is the user a member of the space?"""

        user_list = self.getSpaceUsers(mediaspace_id)
        return username in user_list
