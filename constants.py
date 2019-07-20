#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
""" All of the constants required for lottery_generator.py
    excepting the colour constants
"""
from typing import Any, Dict, List, Optional, Tuple
import pathlib
from versioning import VersionData

Key = str
Name = str

# set the version numbers here and return the string
VERSION = VersionData(name="GenLottery", major=1, minor=0, patch=5)

# names of the various lottery types
LOTTERY_TYPES: List[Name] = [
    "LOTTO",
    "EURO",
    "SET4LIFE",
    "LOTTOHOT",
    "EUROHOT",
    "THUNDER",
]
DEFAULT_TYPE: str = LOTTERY_TYPES[1]  # Currently 'EURO

# Rules for each type of lottery
Data = List[int]
RuleSpec = Dict[Key, Data]
RULES: RuleSpec = {
    # lottery_type: [main_max, main_qty, extra_max, extra_qty]
    LOTTERY_TYPES[0]: [60, 6, False, False],
    LOTTERY_TYPES[1]: [51, 5, 13, 2],
    LOTTERY_TYPES[2]: [48, 5, 11, 1],
    LOTTERY_TYPES[3]: [60, 5, False, False],
    LOTTERY_TYPES[4]: [51, 5, False, False],
    LOTTERY_TYPES[5]: [40, 5, 15, 1],
}

# The smallest number to generate
RULE_START: int = 1

# minimum number of lines to generate
MIN_LINES: int = 1
# maximum number of lines to generate.
# This is an arbitrary but reasonable limit
MAX_LINES: int = 100
# default number of lines to generate
DEFAULT_LINES: int = 2

# path to the saved files
# currently a sub directory of the user's home directory
SAVE_FILE_DIR: str = str(pathlib.Path.home()) + "/lottery-db/"
# filename extension for saved files
SAVE_FILE_TYPE: str = ".db"

# a dictionary of shelf keys
SHELF_ARGS: Dict[Key, Name] = {
    # dictionary key: shelf namespace key
    "DATE": "d",
    "TYPE": "t",
    "LINES": "l",
    "PART1": "x1",
    "PART2": "x2",
}
# protocol to use for saved file
SHELF_PROTOCOL: int = 4
# file mode when reading saved file
SHELF_READONLY: str = "r"

# date display format
DATE_FORMAT: str = "%A %d %B %Y at %X %Z"

# A dictionary of arguments_gui keys to display components
ELEMENT_NAMES: Dict[Key, Name] = {
    "LOTTO": "LOTTO",
    "LINES": "LINES",
    "COUNT": "COUNT",
    "DELETE": "DELETE",
    "SHOW": "SHOW",
    "NOSAVE": "NOSAVE",
    "SAVE": "SAVE",
    "FILENAME": "FILE",
}

GUI_JUSTIFY: str = "right"
GUI_FONT_NAME: str = "Helvetica"
GUI_FONT_SIZE: int = 16

# Results = Dict[int, Tuple[List, Union[List, None]]]
Results = Dict[int, Tuple[List[str], Optional[List[Any]]]]
