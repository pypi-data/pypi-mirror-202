from typing import Final, Dict, Optional

from drill4snap.jobs import ToolJob, DiffMode, Units, ToolJobSegment

HEADER_START = 'M48'
HEADER_END_1 = 'M95'
HEADER_END_2 = '%'
FILE_END = 'M30'
FORMAT_1_LINE: Final = 'FMAT,1'
FORMAT_2_LINE = 'FMAT,2'
UNITS_MM = 'METRIC'
UNITS_INCH = 'INCH'
UNIT_LINE = 'METRIC'
DIFF_MODE_ABSOLUTE = 'G90'
DIFF_MODE_INCREMENTAL = 'G91'
UNIT_BLOCK_MM = 'M71'
UNIT_BLOCK_INCH = 'M72'
DRILL_MODE = 'G05'
MODE_DRILLING = 'G05'
MODE_ROUTING = 'G00'


def is_end_of_header(command: str) -> bool:
    return command == HEADER_END_1 or command == HEADER_END_2


class DrillFileError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class ExcellonFileParser:
    def __init__(self, in_file_path: str):
        self._in_file_path: str = in_file_path
        self._in_file = None
        self._tool_jobs: Dict[int, ToolJob] = {}
        self._active_tool: int = 0
        self._active_job: Optional[ToolJobSegment] = None
        self._diff_mode: Optional[DiffMode] = None
        self._units: Optional[Units] = None
        self._drilling_mode: bool = False

    def parse(self):
        try:
            self._in_file = open(self._in_file_path, 'r')
            self._parse_header()
            self._parse_body()
            return self._tool_jobs
        finally:
            self._in_file.close()

    def _parse_header(self):
        while self._get_next_command() != HEADER_START:
            pass

        while not is_end_of_header(command := self._get_next_command()):
            if command == FORMAT_1_LINE:
                raise DrillFileError('format type 1 not supported')
            elif command == FORMAT_2_LINE:
                pass
            elif command == UNITS_MM:
                self._units = Units.MM
            elif command == UNITS_INCH:
                self._units = Units.INCH
            elif command.startswith('T'):
                self._add_tool(command)
            else:
                print('unknown command', command)

    def _parse_body(self):
        while (command := self._get_next_command()) != FILE_END:
            if command.startswith('T'):
                self._switch_tool(command)
            elif command.startswith('X'):
                self._add_hole(command)
            elif command == DIFF_MODE_ABSOLUTE:
                self._switch_diff_mode(DiffMode.ABSOLUTE)
            elif command == DIFF_MODE_INCREMENTAL:
                self._switch_diff_mode(DiffMode.RELATIVE)
            elif command == UNIT_BLOCK_MM:
                self._switch_units(Units.MM)
            elif command == UNIT_BLOCK_INCH:
                self._switch_units(Units.INCH)
            elif command == MODE_DRILLING:
                self._drilling_mode = True
            elif command == MODE_ROUTING:
                raise DrillFileError('routing mode command found in drill file')
            else:
                print('unsupported command', command)

    def _add_tool(self, command):
        tool_num, diameter = command[1:].split('C')
        tool_num = int(tool_num)
        diameter = float(diameter)
        if tool_num in self._tool_jobs:
            raise DrillFileError(f'tool {tool_num} has multiple definitions')
        self._tool_jobs[tool_num] = ToolJob(diameter=diameter)

    def _switch_units(self, units: Units):
        if units == self._units:
            return
        self._units = units
        self._set_params_changed()

    def _switch_diff_mode(self, diff_mode: DiffMode):
        if diff_mode == self._diff_mode:
            return
        self._diff_mode = diff_mode
        self._set_params_changed()

    def _switch_tool(self, command: str):
        tool_number = int(command[1:])
        if tool_number == self._active_tool:
            return

        if tool_number == 0:
            self._active_tool = 0
            self._active_job = None
            return

        if tool_number not in self._tool_jobs:
            raise DrillFileError(f'tool {tool_number} has not been defined')
        self._active_tool = tool_number
        self._set_params_changed()

    def _add_hole(self, command: str):
        if self._active_tool < 1:
            raise DrillFileError('not tool set for operation')
        if not self._drilling_mode:
            raise DrillFileError('drilling mode not explicitly set')

        x, y = command[1:].split('Y')
        x = float(x)
        y = float(y)

        if self._active_job is None:
            job = ToolJobSegment(
                diff_mode=self._diff_mode,
                units=self._units
            )
            self._tool_jobs[self._active_tool].segments.append(job)
            self._active_job = job

        self._active_job.holes.append((x, y))

    def _set_params_changed(self):
        self._active_job = None

    def _get_next_command(self):
        while (line := self._in_file.readline()) != '':
            line = line.strip('\t\r\n ')
            if line != '' and not line.startswith(';'):
                return line
        raise DrillFileError('unexpected end of file')


__all__ = ['DrillFileError', 'ExcellonFileParser']
