#!/usr/bin/env python3
from enum import Enum
from pathlib import Path

import typer

from drill4snap.parser import ExcellonFileParser
from drill4snap.writer import GcodeWriter


class DeviceTypeArgs(str, Enum):
    s1 = 's1'
    s2s = 's2s'
    s2m = 's2m'
    s2l = 's2l'
    s3 = 's3'


DEVICE_TYPE_ARG_TO_NAME_MAPPING = {
    's1': 'original',
    's2s': 'a150',
    's2m': 'a250',
    's2l': 'a350',
    's3': 'a400',
}


def main(
        height: float = typer.Option(25.0, help='travel height above work origin in mm'),
        power: int = typer.Option(100, help='spindle power [%]'),
        depth: float = typer.Option(2.0, help='drill depth [mm]'),
        sdrill: int = typer.Option(300, help='vertical drill motion speed [mm/min]'),
        smove: int = typer.Option(1500, help='vertical motion speed [mm/min]'),
        stravel: int = typer.Option(1500, help='vertical travel speed when not working [mm/min]'),
        device: DeviceTypeArgs = typer.Option(DeviceTypeArgs.s2l, help='specify the target device (defaults to A350)'),
        drill_file: str = typer.Argument(..., help='Excellon .drl file to convert'),
):
    """
    Convert Excellon drill files to gcode that can be used with the Snapmaker 2.0 CNC family.

    Based on drl2gcode (https://github.com/jes/drl2gcode) by James Stanley
    which is based on
    drl2gcode (https://git.nexlab.net/machinery/drl2gcode) by Franco Lanza.

    Licenced under LGPL
    """

    jobs = ExcellonFileParser(in_file_path=drill_file).parse()
    for tool_job in jobs.values():
        GcodeWriter(
            tool_job, DEVICE_TYPE_ARG_TO_NAME_MAPPING[device],
            spindle_power=power,
            travel_height=height,
            drill_depth=depth,
            drill_speed_z=sdrill,
            travel_speed_z=stravel,
            travel_speed_xy=smove,
        ).write(Path(drill_file).stem)


def cli():
    typer.run(main)
