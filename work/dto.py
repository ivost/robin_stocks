import datetime
import sys

_pv = sys.version_info
if _pv[0] == 3:
    if _pv[1] == 6:
        # if using py 3.6 - backport of 3.7 dataclasses
        from dataclasses import dataclass
    if _pv[1] > 6:
        from attr import dataclass
    else:
        raise Exception("Python >= 3.6 is required")


@dataclass
class Point:
    dt: datetime.datetime
    low: float
    open: float
    close: float
    high: float
    volume: int
