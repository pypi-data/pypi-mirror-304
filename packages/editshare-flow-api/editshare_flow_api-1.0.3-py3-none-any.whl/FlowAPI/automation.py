"""
FLOW Automation service API
See here: https://developers.editshare.com/?urls.primaryName=EditShare%20FLOW%20Automation
"""
import json

from .core import (
    AUTOMATION_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)


class Automation(Connection):
    """Wraps the automation service api"""

    # pylint: disable=too-many-public-methods

    def __init__(self):
        super().__init__()
        self._service_name = "automation"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Automation, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Automation, username, password, ip_addr)

    def connect(self, ip_addr, username, password):
        return Connection.connect2(self, ip_addr, AUTOMATION_PORT, username, password)

    def getTemplates(self):
        """Get all templates"""

        return self.getThatReturnsObj("/templates")

    def findTemplate(self, name):
        """Find the template with the given name"""

        templates = self.getTemplates()
        if templates:
            for template in templates:
                if template["name"] == name:
                    return template
        return None

    def deleteTemplate(self, template):
        return self.deleteThatReturnsBOOL(
            "deleteTemplate", "/templates/" + template["template_uuid"]
        )

    def activeTemplates(self):
        return self.getThatReturnsObj("/templates/instances")

    def getTemplateInstance(self, template_id):
        id_to_use = template_id
        if "template_uuid" in template_id:
            id_to_use = template_id["template_uuid"]
        return self.getThatReturnsObj("/templates/{}/instance".format(id_to_use))

    def getTemplateInstances(self, template_id):
        id_to_use = template_id
        if "template_uuid" in template_id:
            id_to_use = template_id["template_uuid"]
        return self.getThatReturnsObj("/templates/{}/instances".format(id_to_use))

    def getNodes(self):
        return self.getThatReturnsObj("/nodes")

    def getScripts(self):
        return self.getThatReturnsObj("/nodes/scriptrunner/scripts")

    def getQueue(self):
        return self.getThatReturnsObj("/jobs/queue")

    def getJob(self, uuid):
        return self.getThatReturnsObj("/jobs/{}".format(uuid))

    def getJobs(self, start=0, count=50, status=None):
        url = "/jobs?start={}&count={}".format(start, count)
        if status:
            url += "&status={}".format(status)
        return self.getThatReturnsObj(url)

    def updateJobProgress(self, job_id, node_id, progress):
        reply = self.put(
            "/jobs/" + job_id + "/nodes/" + node_id + "?progress=" + str(progress)
        )
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("nodes", reply)

    def triggerTemplate(self, template_id):
        id_to_use = template_id
        if "template_uuid" in template_id:
            id_to_use = template_id["template_uuid"]
        reply = self.put("/templates/" + id_to_use + "/trigger")
        if self.lastReturnCode() != 200:
            return False
        return self.bool_from_reply("trigger", reply)

    def triggerTemplateExternal(self, template_id, data):
        """Trigger a running template
        data is a list of ids like this:
        [{"clip_id": 123}]
        returns uuid of job
        """
        id_to_use = template_id
        if "template_uuid" in template_id:
            id_to_use = template_id["template_uuid"]

        url = "/templates/external/" + id_to_use + "/trigger"
        reply = self.put(url, json.dumps(data))
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def activateTemplate(self, template_id):
        id_to_use = template_id
        if "template_uuid" in template_id:
            id_to_use = template_id["template_uuid"]
        url = "/templates/" + id_to_use + "/activate"
        return self.putThatReturnsBOOL("activateTemplate", url, None)

    def deactivateTemplate(self, template_id, force):
        id_to_use = template_id
        if "template_uuid" in template_id:
            id_to_use = template_id["template_uuid"]

        url = "/templates/" + id_to_use + "/deactivate"
        if force:
            url += "?force=true"
        else:
            url += "?force=false"
        return self.putThatReturnsBOOL("activateTemplate", url, None)

    def testTemplate(self, template_id):
        id_to_use = template_id
        if "template_uuid" in template_id:
            id_to_use = template_id["template_uuid"]

        url = "/templates/" + id_to_use + "/test"
        return self.putThatReturnsBOOL("activateTemplate", url, None)

    def getJobsForInstance(self, instance_id):
        return self.getThatReturnsObj("/jobs/?template={}".format(instance_id))

    def createTemplate(self, template):
        """Create a new template"""

        return self.postThatReturnsObj("/templates", template)

    def get_template(self, template_uuid, validate):
        """Get a template"""

        url = "/templates/" + str(template_uuid)
        if validate:
            url += "?validate=true"
        return self.getThatReturnsObj(url)

    def update_template(self, template_uuid, template_data, validate, refresh):
        """Update template data, optionally validate the data"""

        url = "/templates/" + template_uuid
        if validate:
            url += "?validate=true"
        if refresh:
            url += "?refresh=true"
        self.putThatReturnsBOOL("update_template", url, template_data)

    def set_automation_user(self, username, password: str) -> bool:
        """Set the automation user details"""

        url = "/settings"
        data = {"key": "username", "value": username}
        rv1 = self.putThatReturnsBOOL("set_automation_user", url, data)

        data = {"key": "password", "value": password}
        rv2 = self.putThatReturnsBOOL("set_automation_user", url, data)

        return rv1 and rv2

    def get_setting(self, setting_section, setting_key):
        """Get a setting - TODO move to base class"""

        url = "/settings/{}/{}".format(setting_section, setting_key)
        return self.getThatReturnsObj(url)

    def put_setting(self, setting_section, setting_key, setting_value):
        """Save a setting - TODO move to base class"""

        url = "/settings/" + setting_section + "/" + setting_key
        return self.putThatReturnsBOOL("put_setting", url, setting_value)
