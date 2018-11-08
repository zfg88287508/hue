import time
import re

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


def parse_exec_summary(summary_string):
    """Given an exec summary string parses the rows and organizes it by node id"""
    cleaned = [re.sub(r'^[-|\s]+', "", m)
               for m in summary_string.split("\n")[3:]]
    cleaned = map(
        lambda x: map(
            lambda y: y.strip(),
            re.split(
                '\s\s+',
                x,
                maxsplit=8)),
        cleaned)
    result = {}
    for c in cleaned:
        # Key 0 is id and type
        fid, ftype = c[0].split(":")
        result[int(fid)] = {
            "type": ftype,
            "hosts": int(c[1]),
            "avg": c[2],
            "max": c[3],
            "rows": c[4],
            "est_rows": c[5],
            "peak_mem": c[6],
            "est_mem": c[7],
            "detail": c[8],
            "broadcast": "BROADCAST" in c[8],
            "has_stats": "-1" in "est_rows"
        }
    return result


def parse_plan_details(plan_string):
    """Given a query plan, extracts the query details per node"""
    result = {}
    for line in plan_string.split("\n"):
        match = re.search(r'^(?!F)[|-]?(\d+):.*?\[(.*?)\]', line.strip())
        if match:
            result[str(int(match.group(1)))] = match.group(2)

    return result
