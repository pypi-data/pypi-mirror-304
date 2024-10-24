"""
Class to generate information about a machine such as cpu and memory use

Only works on Linux - it runs top to get the information required
"""
import datetime
import logging
import platform
import shlex
import subprocess
import threading
import time


class Statistics:
    def __init__(self):
        self.wait_idle_time_mins = 0
        self.sample_time_seconds = 10
        self.mem_data_file = open("mem.csv", "w")
        self.cpu_data_file = open("cpu.csv", "w")
        self.sample_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.max_user_cpu = 0.0
        self.max_user_cpu_time = None
        self.max_memory = 0

        # prepare the header lines in the output files
        lineData = "Time,total,free,used,buff/cache\n"
        self.mem_data_file.write(lineData)

        lineData = "Time,us,sy,ni,id,wa,hi,si,st\n"
        self.cpu_data_file.write(lineData)

        self.worker_thread = None
        self.kill_event = threading.Event()
        self.thread_dead = threading.Event()

    def start(self, sample_time_seconds=10, wait_idle_time_mins=0):
        if platform.system().lower() == "windows":
            logging.warning("Statistics module does not work on Windows")
            return
        self.wait_idle_time_mins = wait_idle_time_mins
        self.sample_time_seconds = sample_time_seconds
        self.kill_event.clear()
        self.thread_dead.clear()
        self.worker_thread = threading.Thread(target=self.worker_thread_entry)
        self.worker_thread.start()

    def worker_thread_entry(self):
        while True:
            self.sample_now()

            # print( self.sample_time_seconds )
            if self.kill_event.wait(self.sample_time_seconds):
                # print("kill event set")
                break

        # print("dead event set")
        self.thread_dead.set()

    def stop(self):
        if self.worker_thread:
            # set the event to kill the thread
            self.kill_event.set()
            # wait for the thread to signal it is done
            self.thread_dead.wait()

        # close our data files
        self.mem_data_file.close()
        self.cpu_data_file.close()

        # dump stats
        logging.debug(
            "Max cpu was {} at {}".format(self.max_user_cpu, self.max_user_cpu_time)
        )

    def sample_now(self):
        self.sample_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._getTopInfo()

    # gather information from top
    def _getTopInfo(self):
        # top -b -n1 | grep "%Cpu"

        process = subprocess.Popen(
            # shlex.split(cmd),
            ["top", "-b", "-n1"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        # output = subprocess.call('top -b -n1 | grep "%Cpu"', shell=True)

        # output = output.split()
        # print( output )
        # wait_for_key("Press 'Enter'")

        # print( process.returncode )

        # if process.returncode != 0:
        #    return False

        output = process.communicate()[0]

        useful_lines = 0
        for line in output.splitlines():
            if line.startswith("%Cpu"):
                data = line.split()
                # print( len(data) )
                # print( data )
                # should be 17 items long, like this
                # %Cpu(s):  2.7 us,  0.5 sy,  0.0 ni, 96.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.2 st
                """'
                us, user    : time running un-niced user processes
                sy, system  : time running kernel processes
                ni, nice    : time running niced user processes
                id, idle    : time spent in the kernel idle handler
                wa, IO-wait : time waiting for I/O completion
                hi : time spent servicing hardware interrupts
                si : time spent servicing software interrupts
                st : time stolen from this vm by the hypervisor
                """
                user_cpu = float(data[1])

                if user_cpu > self.max_user_cpu:
                    self.max_user_cpu = user_cpu
                    self.max_user_cpu_time = self.sample_time

                line_data = "{},{},{},{},{},{},{},{},{}".format(
                    self.sample_time,
                    data[1],
                    data[3],
                    data[5],
                    data[7],
                    data[9],
                    data[11],
                    data[13],
                    data[15],
                )
                # print(line_data)
                self.cpu_data_file.write(line_data + "\n")
                self.mem_data_file.flush()
                useful_lines += 1

            elif line.startswith("KiB Mem :"):
                data = line.split()
                # should be 11 items long, like this:
                # KiB Mem :  4037568 total,  1657580 free,  1365984 used,  1014004 buff/cache
                # print( len(data) )
                # print( data )
                line_data = "{},{},{},{},{}".format(
                    self.sample_time, data[3], data[5], data[7], data[9]
                )
                # print(line_data)
                self.mem_data_file.write(line_data + "\n")
                self.mem_data_file.flush()
                useful_lines += 1

            if useful_lines >= 2:
                break


def main():
    stats = Statistics()
    # stats.start(1)

    try:
        while True:
            stats.sample_now()

            time.sleep(2)
            # break
    except KeyboardInterrupt:
        print("ctrl-c")

    print("stopping stats...")
    stats.stop()


if __name__ == "__main__":
    main()
