from dataclasses import dataclass
from typing import Tuple


@dataclass
class Device:
    name: str
    work_area: Tuple[int, int]


DEVICES = [
    Device('Original', (125, 125)),
    Device('A150', (160, 160)),
    Device('A250', (230, 250)),
    Device('A350', (320, 350)),
    Device('A400', (400, 400)),
]

def get_device_by_name(device_name: str):
    for device in DEVICES:
        if device_name.lower() == device.name.lower():
            return device
    raise IndexError