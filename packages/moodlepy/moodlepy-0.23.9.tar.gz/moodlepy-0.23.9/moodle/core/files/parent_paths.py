from typing import List

from moodle import MoodleWarning, ResponsesFactory
from moodle.attr import dataclass, field


@dataclass
class ParentPaths(ResponsesFactory[str]):
    """Parent Paths

    Args
        parentpaths (List[str]): Path to parent directory of the deleted files.
        warnings (List[Warning]): list of warnings
    """

    parentpaths: List[str] = field(factory=list)
    warnings: List[MoodleWarning] = field(factory=list)

    @property
    def items(self) -> List[str]:
        return self.parentpaths
