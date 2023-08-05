from typing import Optional

from moodle.attr import dataclass
from . import CategoryType


@dataclass
class UpdateCohort:
    """arg for core_cohort_update_cohorts

    Args:
        id (str): ID of the cohort
        categorytype (CategoryType): Cohort category / type
        name (str): cohort name
        idnumber (str): cohort idnumber
        description (Optional[str]): cohort description
        descriptionformat (int): Default to "1" description format (1 = HTML, 0 = MOODLE, 2 = PLAIN or 4 = MARKDOWN)
        visible (Optional[int]): cohort visible
        theme (Optional[str]): the cohort theme. The allowcohortthemes setting must be enabled on Moodle
    """

    id: str
    categorytype: CategoryType
    name: str
    idnumber: str
    description: Optional[str] = None
    descriptionformat: int = 1
    visible: Optional[int] = None
    theme: Optional[str] = None
