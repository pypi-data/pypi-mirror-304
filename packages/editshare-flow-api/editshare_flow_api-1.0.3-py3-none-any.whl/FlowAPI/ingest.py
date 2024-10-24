"""
FLOW Ingest service API
See here: https://developers.editshare.com
"""
import json
import logging
import sys
import time

from .core import (
    INGEST_PORT,
    TRANSCODE_PORT,
    Connection,
    create_gateway_instance_inner,
    create_instance,
)


class Ingest(Connection):
    """Wraps the Ingest service api"""

    # pylint: disable=too-many-public-methods

    def __init__(self):
        super().__init__()
        self._service_name = "ingest"

    @staticmethod
    def create_instance(ip_addr, username, password):
        """Create and connect directly to service server"""

        return create_instance(Ingest, ip_addr, username, password)

    @staticmethod
    def create_gateway_instance(username, password, ip_addr=None):
        """Create and connect to service via the local gateway"""

        return create_gateway_instance_inner(Ingest, username, password, ip_addr)

    def connect(self, ip_addr, username, password, transcode_mode=False):
        """Connect ingest server"""

        port = INGEST_PORT
        if transcode_mode:
            port = TRANSCODE_PORT
        return Connection.connect2(self, ip_addr, port, username, password)

    def inputs(self):
        """Get a list of inputs"""

        return self.getThatReturnsObj("/ingest/inputs")

    def getInputTimecode(self, input_id):
        """Get the timecode from an input"""

        return self.get("/ingest/inputs/" + input_id + "/timecode")

    # Wrap the /ingest/outputs endpoint
    def outputs(self):
        return self.getThatReturnsObj("/ingest/outputs")

    def outputsForInput(self, input_uuid, frame_rate):
        """Wrap the /ingest/outputs endpoint"""

        return self.getThatReturnsObj(
            "/ingest/outputs?input_id="
            + input_uuid
            + "&frame_rate="
            + self.safe_url_string(frame_rate)
        )

    def outputsForRate(self, frame_rate):
        return self.getThatReturnsObj(
            "/ingest/outputs?frame_rate=" + self.safe_url_string(frame_rate)
        )

    def getLocationsForOutput(self, output_uuid):
        return self.getThatReturnsObj("/ingest/locations?output_id=" + output_uuid)

    def getOutput(self, output_id):
        return self.getThatReturnsObj("/ingest/outputs/" + str(output_id))

    def getInput(self, input_id):
        return self.getThatReturnsObj("/ingest/inputs/" + str(input_id))

    def channels(self):
        return self.getThatReturnsObj("/ingest/channels")

    def getChannel(self, index):
        reply = self.get("/ingest/channels")
        channel_list = json.loads(reply)
        counter = 0
        for item in channel_list:
            if counter == index:
                return item
            counter += 1
        return None

    def getLocations(self):
        return self.getThatReturnsObj("/ingest/locations")

    def getLocation(self, location_name):
        location_list = self.getLocations()
        if not location_list:
            return None
        for location in location_list:
            # print i['name']
            if location["name"] == location_name:
                return location
        return None

    def createJob(self, job):
        """Create a new ingest job"""

        reply = self.postThatReturnsObj("/ingest/jobs", job)
        if not reply:
            sys.exit(self.lastResponse())
        return reply

    def getJob(self, job_id):
        return self.getThatReturnsObj("/ingest/jobs/" + job_id)

    def deleteJob(self, job_id):
        reply = self.delete("/ingest/jobs/" + job_id)

        # print( reply )
        # print( self.lastReturnCode() )
        #   return False;
        return self.bool_from_reply("deleteCaptureJob", reply)

    def startJob(self, job_id):
        reply = self.put("/ingest/jobs/" + job_id + "/start")
        return self.bool_from_reply("startCaptureJob", reply)

    def getJobState(self, job_id):
        reply = self.getThatReturnsObj("/ingest/jobs/" + job_id + "/state")
        return reply

    def stopJob(self, job_id):
        reply = self.put("/ingest/jobs/" + job_id + "/stop")
        return self.bool_from_reply("stopCaptureJob", reply)

    def getJobTimecode(self, job_id):
        """Get current timecode"""
        return self.get("/ingest/jobs/" + job_id + "/timecode")

    def getJobs(self):
        reply = self.get("/ingest/jobs")
        # print( reply )
        # print( self.lastReturnCode() )
        if self.lastReturnCode() != 200:
            return False
        return json.loads(reply)

    def editJob(self, job):
        reply = self.put("/ingest/jobs/" + job["job_id"], json.dumps(job))
        return self.bool_from_reply("editJob", reply)

    def waitForJobToFinish(self, job_id, sleep_interval_secs=2, timeout_secs=3600):
        """Waits for the job to complete, returns false if the job is not finished or fails"""

        start = time.time()

        while True:
            reply = self.getJobState(job_id)

            if self.lastReturnCode() != 200:
                logging.error(
                    "Failed to get job! code: %d response: %s",
                    self.lastReturnCode(),
                    self.lastResponse(),
                )

                return False

            logging.debug(
                "waitForJobToFinish: time: {0:.2f} state: {1:} ".format(
                    time.time() - start, reply
                )
            )

            if reply == "complete":
                return reply

            if reply == "failed":
                return reply

            time.sleep(sleep_interval_secs)

            if time.time() - start > timeout_secs:
                logging.error("Timeout waiting for rendermaster job to finish")
                return False
