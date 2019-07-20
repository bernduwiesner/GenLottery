# encoding: utf-8
#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Simple version processing

"""
import dataclasses


@dataclasses.dataclass
class VersionData:
    """Dataclass for version data

    """

    name: str = ""
    major: int = 0
    minor: int = 0
    patch: int = 0

    @property
    def version(self) -> str:
        """A version property

            :return: str a populated version
        """
        return f"{self.major}.{self.minor}.{self.patch}"
