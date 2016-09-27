# coding=utf8
import subprocess
import time
import os
import re
import logging
import cgtk_log
from cgtk_os import TemporaryDirectory
from cgtk_config import studio_config

log = cgtk_log.cgtk_log(level=logging.INFO)


class DeadlineSubmission(object):
    def __init__(self):
        object.__init__(self)
        self.job_id = None

        deadline_cfg = studio_config.get('deadline')
        python_cfg = studio_config.get('python')

        self.deadline_path = deadline_cfg.get("path")
        self.executable = python_cfg.get("path")
        self.arguments = '-c "import time; time.sleep(10)"'
        self.cwd = os.getcwd()
        self.environment = {}
        self.details = {"Plugin": "CommandLine",
                        "Name": "",
                        "Comment": '',
                        "Department": 'Automated',
                        "SecondaryPool": '',
                        "Group": "all",
                        "Priority": "50",
                        "TaskTimeoutMinutes": "0",
                        "EnableAutoTimeout": "False",
                        "ConcurrentTasks": "1",
                        "LimitConcurrentTasksToNumberOfCpus": "True",
                        "MachineLimit": "10",
                        "Whitelist": '',
                        "LimitGroups": '',
                        "JobDependencies": "",
                        "OnJobComplete": "Nothing",
                        "Frames": "0",
                        "ChunkSize": "1",
                        "ExtraInfo0": "",
                        }
        pool = deadline_cfg.get('default_pool')
        if pool:
            self.set_pool(pool)

    def set_cwd(self, cwd):
        self.cwd = cwd

    def set_exe(self, exe):
        self.executable = exe

    def set_args(self, args):
        self.arguments = args

    def set_name(self, name):
        self.details['Name'] = name

    def set_pool(self, pool):
        self.details['Pool'] = pool

    def set_frames(self, frames):
        self.details['Frames'] = str(frames)

    def set_chunk_size(self, size):
        self.details['ChunkSize'] = str(size)

    def set_job_dependencies(self, dep):
        self.details['JobDependencies'] = dep

    def create_environment(self, key, value):
        self.environment[key] = value

    def copy_environment(self, key):
        for env in os.environ:
            if env == key:
                self.create_environment(key, os.environ[key])

    def submit(self):
        with TemporaryDirectory() as tempdir:
            job_info, plugin_info = self.set_job_plugin_info(tempdir)
            command = "%s %s %s" % (self.deadline_path, job_info, plugin_info)
            log.info("submitting command %s", command)

            submission_process = subprocess.Popen(command,
                                                  stdin=subprocess.PIPE,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  shell=False)
            submission_process.wait()

            job_id_match = re.compile("job_id=(?P<job_id>[a-z0-9]{24})")
            for out_info in submission_process.stdout:
                match = job_id_match.match(out_info)
                if match:
                    self.job_id = match.groupdict()["job_id"]
                    break
        return self.job_id

    def set_job_plugin_info(self, tempdir):
        job_submission = {
            'Arguments': self.arguments,
            'Executable': self.executable,
            'StartupDirectory': self.cwd,
        }
        job_info = os.path.join(tempdir, "job_info.job")
        for index, key in enumerate(self.environment):
            self.details['EnvironmentKeyValue%s' % index] = "%s=%s" % (key, self.environment[key])

        DeadlineSubmission.write_keys(self.details, job_info)
        plugin_info = os.path.join(tempdir, "info.publin")
        DeadlineSubmission.write_keys(job_submission, plugin_info)
        return job_info, plugin_info

    @staticmethod
    def write_keys(key_pairs, key_file):
        string = ''
        for key in key_pairs:
            string += '%s=%s\n' % (key, key_pairs[key])
        with open(key_file, 'w') as f:
            f.write(string)
        return key_file

    def wait_until_complete(self):
        condition = True
        while condition:
            progress = self.get_job_progress()
            if progress == 100:
                return
            time.sleep(1)

    def get_job_progress(self):
        cmd = self.deadline_path + " GetTaskProgress " + self.job_id
        get_task_process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        get_task_process.wait()
        progress_match = re.compile("JobProgress=(?P<progress>[0-9]+)%")
        for out_info in get_task_process.stdout:
            match = progress_match.match(out_info)
            if match:
                return int(match.groupdict()["progress"])
