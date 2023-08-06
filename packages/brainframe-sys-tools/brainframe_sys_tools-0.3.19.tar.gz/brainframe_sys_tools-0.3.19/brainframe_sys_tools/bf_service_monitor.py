#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
import os
import subprocess
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from pathlib import Path
from subprocess import Popen
from time import sleep, time
from typing import Callable

from brainframe.api import BrainFrameAPI

from brainframe_sys_tools.bf_info import save_sys_info
from brainframe_sys_tools.command_utils import command, subcommand_parse_args, by_name


class HeartBeat:
    def __init__(self, log_path, interval, threshold):

        self.interval = int(interval)
        self.threshold = int(threshold)

        if os.path.isdir(log_path) is not True:
            print(f"{log_path} is invalid!")
            return
        self.log_path = log_path

        self.time_0 = datetime.now()
        self.log_path_prefix = None
        self.heartbeat_log_file = None
        self.brainframe_log_filename = None
        self.heartbeat_log_open(interval, threshold)

    def heartbeat_log_open(self, interval, threshold):
        self.time_0 = datetime.now()
        self.log_path_prefix = str(self.log_path) + f"/{self.time_0.isoformat()}_"
        self.brainframe_log_filename = self.log_path_prefix + "brainframe.log"

        log_filename = self.log_path_prefix + "brainframe_heartbeat.log"
        self.heartbeat_log_file = Path(log_filename).resolve().open(mode="a")

        self.heartbeat_log(
            f"BrainFrame HeartBeat starts, interval = {interval}, threshold = {threshold}"
        )

    def heartbeat_log_close(self):
        self.heartbeat_log(
            f"BrainFrame HeartBeat session closed, {datetime.now() - self.time_0}"
        )
        self.heartbeat_log_file.close()

    def heartbeat_log(self, log_str):
        _log_str = f"[{datetime.now()}] " + str(log_str) + "\n"
        print(_log_str)
        self.heartbeat_log_file.writelines(_log_str)
        self.heartbeat_log_file.flush()

    def restart_brainframe(self):
        self.heartbeat_log(f"Stop brainframe")
        self.save_brainframe_logs()
        brainframe_sys_info_filename = self.log_path_prefix + "sys.info"
        save_sys_info(brainframe_sys_info_filename)
        self.stop_brainframe()
        self.heartbeat_log(f"Save brainframe logs at {self.brainframe_log_filename}")
        self.heartbeat_log_close()

        self.heartbeat_log_open(self.interval, self.threshold)
        self.heartbeat_log(f"Start brainframe")
        self.start_brainframe()
        self.heartbeat_log("brainframe has started")

    def process_helper(self, cmd_str):
        execution_start_time = datetime.now()
        self.heartbeat_log(f"{cmd_str}: [{execution_start_time}]")
        p = Popen(
            cmd_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True,
            start_new_session=True,
            close_fds=True,
        )
        # output = p.stdout.read()
        output, err = p.communicate()
        p.wait()
        execution_complete_time = datetime.now()
        self.heartbeat_log(f"{cmd_str} completed: [{execution_complete_time}]")

        brainframe_log_file = (
            Path(self.brainframe_log_filename).resolve().open(mode="a")
        )
        brainframe_log_file.writelines(f"[{execution_start_time}] {cmd_str}: stdout\n")
        brainframe_log_file.writelines(output)
        brainframe_log_file.writelines(f"[{execution_start_time}] {cmd_str}: stderr\n")
        brainframe_log_file.writelines(err)
        brainframe_log_file.writelines(f"[{execution_complete_time}] {cmd_str}\n")
        brainframe_log_file.close()

        self.heartbeat_log(f"Output are saved to {self.brainframe_log_filename}\n")

    def save_brainframe_logs(self):
        # os.system(f"brainframe compose logs &>> {log_filename}", )
        cmd_str = ["brainframe compose logs"]
        self.process_helper(cmd_str)

    def stop_brainframe(self):
        # os.system(f"brainframe compose down &>> {log_filename}")
        cmd_str = ["brainframe compose down"]
        self.process_helper(cmd_str)

    def start_brainframe(self):
        # os.system(f"brainframe compose up -d &>> {log_filename}")
        cmd_str = ["brainframe compose up -d"]
        self.process_helper(cmd_str)

    def wait_for_heartbeat(self, fn: Callable, timeout: float = None):
        """A helpful function to wait for heartbeat."""
        heartbeat_val, heartbeat_response = None, None
        start_time = time()
        while timeout is None or time() - start_time < timeout:
            try:
                heartbeat_response = fn()
                heartbeat_val = time() - start_time
                break
            except:
                heartbeat_val = time() - start_time
                break

        return heartbeat_val, heartbeat_response

    def heartbeat_monitor(self, api):
        has_restarted = False
        while True:
            heartbeat_val, heartbeat_response = self.wait_for_heartbeat(
                lambda: api.version(self.threshold), self.threshold
            )
            if heartbeat_response:
                has_restarted = False
                self.heartbeat_log(
                    f"version {heartbeat_response} heartbeat OK: response time - {heartbeat_val}"
                )
            else:
                self.heartbeat_log(f"heartbeat failed: timeout - {heartbeat_val}")
                if not has_restarted:
                    self.restart_brainframe()
                    has_restarted = True

            sleep(self.interval)


def _parse_args():
    parser = ArgumentParser(
        description="This is the brainframe service monitor. Run the command with no arguments will launch"
        " brainframe service and monitor the brainframe heartbeats. It will restart the service"
        " when the heartbeats are not observed in the given timeout threshold. For example, run"
        " the command below will monitor the heartbeats at an interval of 5 seconds. The command"
        " will not launch brainframe automatically as '--start-now' is specified.\n\n"
        "    python brainframe_service_monitor.py --log-path ~/workspace --interval 2 --threshold 6 --start-now False\n\n"
        "If the communication with brainframe fails, or a heartbeat deplay exceeds 6 seconds, the"
        " service monitor will save the following log files in ~/workspace directory, then restart"
        " the brainframe service,\n\n"
        "    <timestamp>_hearbeat.log\n"
        "    <timestamp>_brainframe.log\n"
        "    <timestamp>_sys.info\n\n"
        "The default heartbeat interval and timeout threshold can be found in the arguments'"
        " description.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--server-url",
        default="http://localhost",
        help="The URL for the BrainFrame server.",
    )
    parser.add_argument(
        "--interval",
        default=120,
        help="The heartbeat checking interval. Default: %(default)i",
    )
    parser.add_argument(
        "--threshold",
        default=360,
        help="The heartbeat timeout threshold. The service monitor will restart when the communication fails or timeout."
        " Default: %(default)i",
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default="./",
        help="The logs will be saved in this path. Default: %(default)s",
    )
    parser.add_argument(
        "--start-now",
        default=True,
        help="Start the brainframe service. Default: %(default)s",
    )

    args = subcommand_parse_args(parser)
    return args


@command("service_monitor")
def service_monitor():
    args = _parse_args()

    # Connect to the BrainFrame Server
    server_url = args.server_url

    hb = HeartBeat(args.log_path, args.interval, args.threshold)

    if args.start_now:
        hb.start_brainframe()

    hb.heartbeat_log(
        f"heartbeat Connecting: BrainFrameAPI({server_url}), wait_for_server_initialization() ..."
    )
    api = BrainFrameAPI(server_url)
    api.wait_for_server_initialization()

    hb.heartbeat_log("heartbeat Connected")

    hb.heartbeat_monitor(api)

    hb.heartbeat_log("heartbeat exit")


if __name__ == "__main__":
    by_name["service_monitor"]()

