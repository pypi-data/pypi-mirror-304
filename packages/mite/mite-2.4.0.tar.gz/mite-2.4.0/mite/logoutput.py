import logging
import math
import statistics
import time
from collections import defaultdict


class MsgOutput:
    def __init__(self, opts):
        self._logger = logging.getLogger("MSG")

    def process_message(self, msg):
        stacktrace = msg.pop("stacktrace", None)
        if stacktrace and self._logger.isEnabledFor(logging.WARNING):
            message = msg.pop("message", None)
            ex_type = msg.pop("ex_type", None)
            start = f'[{msg.pop("type", None)}] {msg.pop("time", None):.6f}'
            end = ", ".join(f"{k}={v}" for k, v in sorted(msg.items()))
            self._logger.warning(
                "%s %s\n%s: %s\n%s", start, end, ex_type, message, stacktrace
            )
        elif self._logger.isEnabledFor(logging.DEBUG):
            start = f'[{msg.pop("type", None)}] {msg.pop("time", None):.6f}'
            end = ", ".join(f"{k}={v}" for k, v in sorted(msg.items()))
            self._logger.debug("%s %s", start, end)


class DebugMessageOutput:
    def __init__(self, opts):
        self._logger = logging.getLogger("Debug Logger")

    def process_message(self, message):
        text = message.get("text")
        if message.get("type") == "debug_console_message" and text:
            self._logger.info(text)


class GenericStatsOutput:
    def __init__(self, opts, period=2):
        self._period = period
        # get the state of the journey_logging attribute from the
        # opts dictionary
        self._journey_logging = opts.get("--journey-logging", False)
        if self._journey_logging is not False:
            self._journey_logging = True
        self._hide_constant_logs = opts.get("--hide-constant-logs")
        self._report = opts.get("--report")
        self._logger = logging.getLogger(f"{self.log_name} Stats")
        self._init_time = time.time()
        self._start_t = None
        self._req_total = 0
        self._req_recent = 0
        self._error_total = 0
        self._error_recent = 0
        self._resp_time_recent = []
        self._resp_time_min = 0
        self._resp_time_max = 0
        self._resp_time_mean = 0
        self._resp_time_store = []
        self._req_sec_store = []
        self._req_sec_min = 0
        self._req_sec_max = 0
        self._scenarios_completed_time = 0
        self._data_transferred = 0
        self._standard_deviation = 0
        self._error_journeys = defaultdict(int)

    def _pct(self, percentile):
        """Percentile calculation with linear interpolation.

        If the samples have an exact split at `percentile`, return that single
        value; otherwise interpolate the nearest two values.

        Requires that `self._resp_time_recent` is sorted.

        """
        if not self._resp_time_recent:
            return "None"
        assert 0 <= percentile <= 100
        index = (percentile / 100) * (len(self._resp_time_recent) - 1)
        fractional_index, index = math.modf(index)
        index = int(index)
        if fractional_index == 0:
            return f"{self._resp_time_recent[index]}:.6f"
        a = self._resp_time_recent[index]
        b = self._resp_time_recent[index + 1]
        interpolated_amount = (b - a) * fractional_index
        return f"{a + interpolated_amount:.6f}"

    @property
    def error_total(self):
        return self._error_total

    def print_output(self, t):
        dt = t - self._start_t
        self._resp_time_recent.sort()
        if not self._hide_constant_logs:
            self._logger.info(f"Total> #Reqs:{self._req_total} #Errs:{self._error_total}")
        # only output journey logs if the --journey_logging switch is set
        if self._journey_logging:
            for k, v in self._error_journeys.items():
                self._logger.info(f"Total errors for {k} :{v}")
        if not self._hide_constant_logs:
            self._logger.info(
                f"Last {self._period} Secs> #Reqs:{self._req_recent} #Errs:{self._error_recent} "
                + f"Req/S:{self._req_recent / dt:.1f} min:{self._pct(0)} "
                + f"25%:{self._pct(25)} 50%:{self._pct(50)} 75%:{self._pct(75)} "
                + f"90%:{self._pct(90)} 99%:{self._pct(99)} 99.9%:{self._pct(99.9)} "
                + f"max:{self._pct(100)}",
            )
        self._start_t = t
        del self._resp_time_recent[:]
        self._req_recent = 0
        self._error_recent = 0

    def process_message(self, message):
        if "type" not in message:
            return
        msg_type = message["type"]
        t = time.time()
        if self._start_t is None:
            self._start_t = t
        if self._start_t + self._period < t:

            if self._resp_time_recent:
                self._resp_time_store.extend(self._resp_time_recent)
                if self._resp_time_min == 0:
                    self._resp_time_min = self.min_resp_time_recent
                else:
                    self._resp_time_min = min(
                        self.min_resp_time_recent, self._resp_time_min
                    )

                self._resp_time_max = max(self.max_resp_time_recent, self._resp_time_max)

            if self._req_recent:
                req_sec = self._req_recent / (t - self._start_t)
                if self._report:
                    self._req_sec_store.append(req_sec)
                if self._req_sec_min == 0:
                    self._req_sec_min = req_sec
                else:
                    self._req_sec_min = min(req_sec, self._req_sec_min)

                self._req_sec_max = max(req_sec, self._req_sec_max)

            self.print_output(t)
        if msg_type in self.message_types:
            self._resp_time_recent.append(message["total_time"])
            self._data_transferred += message.get("download_size", 0)
            self._req_total += 1
            self._req_recent += 1
        elif msg_type in ("error", "exception"):
            self._error_total += 1
            self._error_recent += 1
            if self._journey_logging:
                journey_name = message.get("journey")
                self._error_journeys[journey_name] += 1

    @property
    def mean_resp_time(self):
        if not self._resp_time_store:
            return 0
        return statistics.fmean(self._resp_time_store)

    @property
    def max_resp_time_recent(self):
        if not self._resp_time_recent:
            return 0
        return max(self._resp_time_recent)

    @property
    def min_resp_time_recent(self):
        if not self._resp_time_recent:
            return 0
        return min(self._resp_time_recent)

    @property
    def req_sec_mean(self):
        if self._req_total == 0:
            return 0
        return statistics.fmean(self._req_sec_store)

    @property
    def resp_time_standard_deviation(self):
        if not self._resp_time_store:
            return 0
        return statistics.stdev(self._resp_time_store)

    @property
    def req_sec_standard_deviation(self):
        if self._req_total == 0:
            return 0
        return statistics.stdev(self._req_sec_store)

    # Calculating percentage of resp times that lie within deviation limits (Mean +/- Standard deviation)
    @property
    def resp_time_within_standard_deviation(self):
        if not self._resp_time_store:
            return 0
        return (
            sum(
                abs(x - self.mean_resp_time) < self.resp_time_standard_deviation
                for x in self._resp_time_store
            )
            / len(self._resp_time_store)
            * 100
        )

    # Calculating percentage of req/sec that lie within deviation limits (Mean +/- Standard deviation)
    @property
    def req_sec_within_standard_deviation(self):
        if self._req_total == 0:
            return 0
        return (
            sum(
                abs(x - self.req_sec_mean) < self.req_sec_standard_deviation
                for x in self._req_sec_store
            )
            / len(self._req_sec_store)
            * 100
        )


class HttpStatsOutput(GenericStatsOutput):
    message_types = {
        "http_metrics",
        "selenium_page_load_metrics",
        "selenium_network_resource_metrics",
    }
    log_name = "Http"


class FinagleStatsOutput(GenericStatsOutput):
    message_types = {"finagle_metrics"}
    log_name = "Finagle"
