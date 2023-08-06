import base64
import dataclasses
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Final, TextIO, Optional, Tuple, Generator

import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL.ImageDraw import ImageDraw

from .devices import get_device_by_name
from .jobs import Units, DiffMode, ToolJob
from .templates import HEADER_TEMPLATE, FOOTER_TEMPLATE, DRILL_TEMPLATE


MM_PER_INCH = 25.4


@dataclass
class JobConfinement:
    min_x: float = 0
    max_x: float = 0
    min_y: float = 0
    max_y: float = 0
    min_z: float = 0
    max_z: float = 0

    def expand_plane(self, x: float, y: float):
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)


def generate_thumbnail(drill_diameter: float):
    thumb_width = 720
    thumb_height = 480
    text_spacing = 10
    text_color = (100, 100, 255, 255)
    text_1 = 'PCB'
    text_2 = f'Ø = {drill_diameter}mm'

    with Image.open(Path(__file__).parent.resolve() / 'drill_pict.png') as icon:
        fnt = ImageFont.truetype('DejaVuSans.ttf', size=100)
        im = Image.new(mode="RGBA", size=(720, 480))
        painter = ImageDraw(im)
        _, _, text_1_width, text_1_height = painter.textbbox((0, 0), text_1, font=fnt)
        text_1_pos = (
            (thumb_width - icon.width - text_1_width) // 2 + icon.width,
            (thumb_height - text_1_height) // 2 - text_spacing - text_1_height // 2,
        )
        painter.text(text_1_pos, text_1, font=fnt, fill=text_color)
        _, _, text_2_width, text_2_height = painter.textbbox((0, 0), text_2, font=fnt)
        text_2_pos = (
            (thumb_width - icon.width - text_2_width) // 2 + icon.width,
            (thumb_height - text_2_height) // 2 + text_spacing + text_2_height // 2,
        )
        painter.text(text_2_pos, text_2, font=fnt, fill=text_color)

        buffered = BytesIO()
        im.paste(icon)
        im.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('ascii')


def iter_holes(job: ToolJob) -> Generator[Tuple[float, float], None, None]:
    # always starts at work origin (0, 0)
    prev_x = 0.0
    prev_y = 0.0

    for segment in job.segments:
        if not segment.holes:
            continue

        for x, y in segment.holes:
            if segment.units == Units.INCH:
                x *= MM_PER_INCH
                y *= MM_PER_INCH
            if segment.diff_mode == DiffMode.RELATIVE:
                x += prev_x
                y += prev_y

            yield x, y

            prev_x = x
            prev_y = y


class MetricsAccumulator:
    def __init__(self, drill_depth: float, travel_height: float, drill_speed_z: float, travel_speed_xy: float):
        self._lines_for_drilling = DRILL_TEMPLATE.count('\n')
        self.drill_speed_z: Final = drill_speed_z
        self._travel_speed_xy: Final = travel_speed_xy

        self._pos = np.array([0, 0])
        self._units: Units = Units.MM
        self._diff_mode = DiffMode.ABSOLUTE

        self._confinement: Final = JobConfinement(min_z=-drill_depth, max_z=travel_height)
        self._lines: int = HEADER_TEMPLATE.count('\n') + FOOTER_TEMPLATE.count('\n') + 1
        self._time: float = 0.0

    @property
    def confinement(self):
        return self._confinement

    @property
    def lines(self):
        return self._lines

    @property
    def time(self):
        return self._time

    def add_drill(self, x: float, y: float):
        volume = self._confinement
        self._confinement.expand_plane(x, y)
        self._lines += self._lines_for_drilling

        # feed rates are provided in mm/min
        travel_time = np.linalg.norm(np.array([x, y]) - self._pos) / self._travel_speed_xy * 60
        drill_time = 2 * (volume.max_z - volume.min_z) / self.drill_speed_z * 60
        self._time += travel_time + drill_time


class GcodeWriter:
    def __init__(
            self, job: ToolJob, device_name: str, *,
            spindle_power: int = 100,
            travel_height: float = 25,
            drill_depth: float = 2,
            drill_speed_z: int = 300,
            travel_speed_z: int = 5000,
            travel_speed_xy: int = 30000,
    ):
        self._job: Final = job
        self._device = get_device_by_name(device_name)
        self._spindle_power: Final = spindle_power
        self._travel_height: Final = travel_height
        self._drill_depth: Final = drill_depth
        self._drill_speed_z: Final = drill_speed_z
        self._travel_speed_z: Final = travel_speed_z
        self._travel_speed_xy: Final = travel_speed_xy

    def write(self, out_file_name: str):
        job = self._job
        with open(f'{out_file_name}_{job.diameter}.cnc', 'w') as out_file:
            metrics = self._determine_metrics()

            self._write_header(out_file, metrics)
            self._write_commands(out_file)
            self._write_footer(out_file)

    def _determine_metrics(self) -> MetricsAccumulator:
        acc = MetricsAccumulator(self._drill_depth, self._travel_height, self._drill_speed_z, self._travel_speed_xy)
        for x, y in iter_holes(self._job):
            acc.add_drill(x, y)
        return acc

    def _write_header(self, out_file: TextIO, acc: MetricsAccumulator):
        thumbnail = generate_thumbnail(self._job.diameter)
        work_area_x, work_area_y = self._device.work_area
        out_file.write(HEADER_TEMPLATE.format(
            device_name=self._device.name,
            lines=acc.lines, time=acc.time,
            drill_diameter=self._job.diameter,
            spindle_power=self._spindle_power,
            drill_speed_z=self._drill_speed_z,
            travel_speed_z=self._travel_speed_z,
            travel_speed_xy=self._travel_speed_xy,
            travel_height=self._travel_height,
            work_area_x=work_area_x, work_area_y=work_area_y,
            thumbnail=thumbnail,
            **dataclasses.asdict(acc.confinement),
        ))

    def _write_footer(self, out_file: TextIO):
        out_file.write(FOOTER_TEMPLATE.format(
            travel_height=self._travel_height,
            travel_speed_z=self._travel_speed_z
        ))

    def _write_commands(self, out_file: TextIO):
        for x, y in iter_holes(self._job):
            out_file.write(DRILL_TEMPLATE.format(
                x=x, y=y,
                drill_speed_z=self._drill_speed_z,
                drill_depth=self._drill_depth,
                travel_speed_xy=self._travel_speed_xy,
                travel_height=self._travel_height,
            ))


__all__ = ['GcodeWriter']
