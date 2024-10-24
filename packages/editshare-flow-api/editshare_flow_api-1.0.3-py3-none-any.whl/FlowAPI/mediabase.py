"""
Imagine Communications MB Rest API
Rest API for accessing data in the media base backend
"""

import json

from .core import Connection, create_instance

MB_PORT = 4078
MB_API_ROOT = "MediaBase"
MB_QL_ROOT = "GraphQL"


class MediaBase(Connection):
    """Wraps the MB Rest API"""

    def __init__(self):
        super().__init__()
        self._gateway_prefix = "/api/"
        self._service_name = ""
        self._content_type = "application/json"

    @staticmethod
    def create_instance(ip_addr):
        """Create and connect directly to service server"""

        return create_instance(MediaBase, ip_addr, "username", "password")

    def connect(self, ip_addr, username, password):
        """Connect"""

        # pylint: disable=unused-argument

        Connection.connect(self, ip_addr, MB_PORT)
        self._use_gateway = True

    def version(self):
        """API Version"""

        reply = self.get(MB_API_ROOT + "/version")
        if self.last_return_code() != 200:
            return False
        return reply

    def update_clip_metadata(
        self,
        clip_name,
        *,
        description=None,
        agency=None,
        mb_type=None,
        mb_title=None,
        department=None,
        user_field1=None,
        user_field2=None,
        user_field3=None,
        user_field4=None,
    ) -> bool:
        """Update a clip's metadata

        Note: I found calling this method with a clip name that does not exist
        hangs it. Please check the clip exists first by calling find_clip_by_name

        :returns: boolean, True if update was successful
        """
        # pylint: disable=too-many-arguments

        metadata = {}

        if description:
            metadata["Description"] = description
        if agency:
            metadata["Agency"] = agency
        if mb_type:
            metadata["Type"] = mb_type
        if mb_title:
            metadata["Title"] = mb_title
        if department:
            metadata["Department"] = department
        if user_field1:
            metadata["UserField1"] = user_field1
        if user_field2:
            metadata["UserField2"] = user_field2
        if user_field3:
            metadata["UserField3"] = user_field3
        if user_field4:
            metadata["UserField4"] = user_field4

        url = MB_API_ROOT + "/registermetadata?name={}&wait=true".format(clip_name)
        self.post(url, metadata)
        return self.last_return_code() == 200

    def find_clip_by_name(self, clip_name):
        """Find a clip from its name

        :returns: A dict of the details or an empty dict if the clip was not found
        """

        query_string = '{"query":"{\n'
        query_string += (
            'allClips(where: [{path: \\"name\\", comparison: contains, value: \\"'
        )
        query_string += clip_name
        query_string += '\\", case_insensitive: true}]) {'
        query_string += "\nname handle duration startTimeCode durationTimeCode"
        query_string += """ metadata {
    agency
    codecName
    department
    description
    link
    title
    type
    userField1
    userField2
    userField3
    userField4
    userName
}"""
        query_string += "\n}"  # End allClips
        query_string += '\n}"'  # End Query
        query_string += "\n}"  # End Body

        # print(query_string)
        # print(query_string.encode("ascii"))

        # with open("whatwesend", "wb") as file_handle:
        #     file_handle.write(query_string.encode())

        reply = self.post(MB_QL_ROOT, query_string.encode())
        if self.last_return_code() != 200:
            return {}
        obj = json.loads(reply)
        all_clips_list = obj["data"]["allClips"]
        if len(all_clips_list) < 1:
            return {}
        return all_clips_list[0]
