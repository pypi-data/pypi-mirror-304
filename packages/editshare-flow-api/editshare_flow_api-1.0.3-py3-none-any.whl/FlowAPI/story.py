# FlowAPI / Story
import json

from .core import Connection


class Story(Connection):
    """Wraps the story server"""

    # Connect to api server
    def connect(self, ip):
        return Connection.connect(self, ip, 61070)

    def createJob2(self, job):
        reply = self.post("/renders/jobs", json.dumps(job))
        # print reply
        if self.lastReturnCode() != 200:
            return False
        obj = json.loads(reply)
        if "job_id" not in obj:
            return False
        return obj["job_id"]

    def createJob(self, project_uuid, sequence_uuid, overwrite, outFiles):
        job = {
            "project_uuid": project_uuid,
            "sequence_uuid": sequence_uuid,
            # "mediaspace_uuid" : ms_uuid,
            "video_preset": "default",
            "overwrite": overwrite,
            "target": {
                "files": outFiles,
                # "mediaspace_uuid" : ms['uuid']
            },
        }

        print(json.dumps(job, sort_keys=True, indent=2, separators=(",", ": ")))
        return self.createJob2(job)

    def getJob(self, jobId):
        rv = self.getThatReturnsObj("/renders/jobs/" + jobId)
        return rv

    def ping(self):
        rv = self.getThatReturnsObj("/ping")
        return rv

    def quit(self):
        rv = self.put("/quit")
        return rv

    def getAllJobs(self):
        rv = self.getThatReturnsObj("/renders/jobs")
        return rv

    def getProjects(self):
        rv = self.getThatReturnsObj("/projects")
        return rv

    def deleteJob(self, jobId):
        reply = self.delete("/renders/jobs/" + jobId)
        if self.lastReturnCode() != 200:
            return False
        return True
