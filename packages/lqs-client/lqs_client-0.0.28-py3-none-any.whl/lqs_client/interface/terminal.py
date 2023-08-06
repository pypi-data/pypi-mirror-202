import os
import time
import datetime
import threading
import argparse
import logging

logging.basicConfig(
    level=os.getenv("LQS_LOG_LEVEL") or logging.INFO,
    format="%(asctime)s  (%(levelname)s - %(name)s): %(message)s",
)
logger = logging.getLogger(__name__)

try:
    from sshkeyboard import listen_keyboard, stop_listening
except ImportError:
    print("Install sshkeyboard for keyboard input")

    def listen_keyboard(*args, **kwargs):
        pass

    def stop_listening(*args, **kwargs):
        pass


try:
    from colorama import Fore, Style, init

    init(autoreset=True)
except ImportError:
    print("Install colorama for colored output")

    class Dummy:
        def __getattr__(self, name):
            return ""

    Fore = Dummy()
    Style = Dummy()


class Terminal:
    def __init__(self, getter, lister, config):
        self._get = getter
        self._list = lister
        self._config = config

    def _format_spdlog_data(self, record, single_line=False):
        data = record["message_data"]
        timestamp = datetime.datetime.fromtimestamp(data["time"] / 1e9).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]
        level = {
            1: "trace",
            2: "debug",
            3: "info",
            4: "warn",
            5: "error",
            6: "critical",
            7: "off",
        }.get(data["level"], "unknown")
        level_colors = {
            "trace": Fore.WHITE,
            "debug": Fore.CYAN,
            "info": Fore.GREEN,
            "warn": Fore.YELLOW,
            "error": Fore.RED,
            "critical": Fore.RED + Style.BRIGHT,
            "unknown": Fore.MAGENTA,
        }
        thread_id = data["thread_id"]
        logger_name = data["logger_name"] if data["logger_name"] else "root"
        payload = data["payload"]
        if payload and single_line:
            payload = payload.replace("\n", "")

        print(
            f"{timestamp} [{level_colors[level]}{level}{Style.RESET_ALL}] [{thread_id}] [{logger_name}] {payload}"
        )

    def _load_data(
        self,
        log_id,
        topic_id,
        offset,
        data_filter=None,
        timestamp_gte=None,
        timestamp_lte=None,
    ):
        return self._list.records(
            log_id=log_id,
            topic_id=topic_id,
            offset=offset,
            limit=100,
            data_filter=data_filter,
            timestamp_gte=timestamp_gte,
            timestamp_lte=timestamp_lte,
        )["data"]

    def play(
        self,
        log_id=None,
        log_name=None,
        topic_id=None,
        topic_name=None,
        data_filter_val="%%",
        max_dt=0.1,
        min_dt=0.01,
        single_line=True,
        paused=False,
        offset=0,
        start_timestamp=None,
        end_timestamp=None,
        start_datetime=None,
        end_datetime=None,
    ):
        if log_name:
            log_id = self._list.logs(name=log_name)["data"][0]["id"]
        elif log_id:
            log_name = self._get.log(log_id=log_id)["data"]["name"]
        else:
            raise Exception("Must provide log_id or log_name")

        if topic_name:
            topic_id = self._list.topics(log_id=log_id, name=topic_name)["data"][0][
                "id"
            ]
        elif topic_id:
            topic_name = self._get.topic(log_id=log_id, topic_id=topic_id)["data"][
                "name"
            ]
        else:
            raise Exception("Must provide topic_id or topic_name")

        if data_filter_val:
            data_filter = {"var": "payload", "op": "ilike", "val": data_filter_val}
        else:
            data_filter = None

        if start_datetime:
            start_timestamp = datetime.datetime.fromisoformat(
                start_datetime
            ).timestamp()
        if end_datetime:
            end_timestamp = datetime.datetime.fromisoformat(end_datetime).timestamp()

        logger.info(f"Log: {log_name} ({log_id})")
        logger.info(f"Topic: {topic_name} ({topic_id})")
        if start_timestamp:
            logger.info(f"Start timestamp: {start_timestamp}")
        if end_timestamp:
            logger.info(f"End timestamp: {end_timestamp}")
        if data_filter:
            logger.info(f"Data filter: {data_filter}")

        self.offset = offset

        # Controls

        self.paused = paused
        self.next = False
        self.prev = False
        self.exit_loop = False

        async def handle_pause(key):
            if key == "space":
                self.paused = not self.paused
            if key == "q":
                self.exit_loop = True
            if key == "s" or key == "up" or key == "left":
                self.prev = True
            if key == "d" or key == "down" or key == "right":
                self.next = True

        threading.Thread(
            target=listen_keyboard,
            kwargs=dict(on_press=handle_pause, delay_second_char=0.1),
        ).start()

        # Record Accumulator
        self.buffer_index = 0
        self.record_buffer = []

        def load_record_buffer():
            while True and not self.exit_loop:
                buffer_len = len(self.record_buffer)
                if buffer_len >= 300 and self.buffer_index > buffer_len - 100:
                    self.record_buffer = self.record_buffer[100:]
                    self.buffer_index -= 100
                    buffer_len = len(self.record_buffer)
                if buffer_len < 300:
                    records = self._load_data(
                        log_id=log_id,
                        topic_id=topic_id,
                        offset=self.offset,
                        data_filter=data_filter,
                        timestamp_gte=start_timestamp,
                        timestamp_lte=end_timestamp,
                    )
                    if len(records) == 0:
                        records = [{"end": True}]
                    self.record_buffer += records
                    if records[-1].get("end"):
                        break
                    self.offset += 100
            return

        thread = threading.Thread(target=load_record_buffer)
        thread.start()

        # Main Loop
        previous_timestamp = None
        logger.info(
            "Press space to pause/resume, q to quit, up/left to go back, down/right to go forward"
        )
        logger.info("Loading data...")
        load_loops = 0
        try:
            while True and not self.exit_loop:
                if len(self.record_buffer) == 0:
                    time.sleep(1)
                    load_loops += 1
                    if load_loops == 30:
                        logger.error(
                            "Still loading data this long indicates an error.  Retry."
                        )
                    continue

                if not self.paused or self.next:
                    next = False
                    self.buffer_index += 1
                    if self.buffer_index >= len(self.record_buffer):
                        self.buffer_index = len(self.record_buffer) - 1
                    record = self.record_buffer[self.buffer_index]
                    if record.get("end"):
                        logger.info("End of data")
                        self.exit_loop = True
                        break

                    timestamp = record["timestamp"]
                    if timestamp == previous_timestamp:
                        continue
                    self._format_spdlog_data(record, single_line=single_line)
                    # print(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                    if not self.paused:
                        if previous_timestamp:
                            dt = timestamp - previous_timestamp
                            if max_dt and dt > max_dt:
                                time.sleep(max_dt)
                            elif min_dt and dt < min_dt:
                                time.sleep(min_dt)
                            else:
                                time.sleep(dt)
                    previous_timestamp = timestamp

                if self.prev:
                    self.prev = False
                    self.buffer_index -= 1
                    if self.buffer_index < 0:
                        self.buffer_index = 0
                    record = self.record_buffer[self.buffer_index]
                    timestamp = record["message_data"]["time"] / 1e9
                    print(
                        datetime.datetime.fromtimestamp(timestamp).strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        )[:-3]
                    )
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.exit_loop = True
            stop_listening()
            thread.join()
            raise e

        logger.info("Waiting for threads to finish...")
        self.exit_loop = True
        stop_listening()
        thread.join()
        logger.info("Done")
