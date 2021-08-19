from typing import Optional
from typing import Union
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from json.decoder import JSONDecodeError

from requests import get
from requests import post
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

from bs4 import BeautifulSoup
from bs4.element import Tag

from bot.models.groups_of_students import GroupsOfStudents
from bot.models.compact_students import CompactStudents
from bot.models.bb_students import BBStudents
from bot.models.settings import Settings

from bot.utilities.api.helpers.schedule import beautify_classes
from bot.utilities.api.helpers.schedule import beautify_exams
from bot.utilities.api.helpers.scoretable import beautify_scoretable
from bot.utilities.api.constants import SCHEDULE_URL
from bot.utilities.api.constants import SCORE_URL
from bot.utilities.api.constants import P_SUB
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.types import ResponseError


def get_group_schedule_id(group: str) -> Tuple[Optional[str], Optional[ResponseError]]:
    try:
        groups: List[Dict[str, str]] = get(url=SCHEDULE_URL, timeout=12, params={
            "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "getGroupsURL",
            "query": group
        }).json()
    except (ConnectionError, Timeout, JSONDecodeError):
        return (None, ResponseError.NO_RESPONSE)
    
    if len(groups) != 1 or "id" not in groups[0]:
        return (None, ResponseError.NO_DATA)
    
    return (groups[0]["id"], None)

def get_schedule_by_group_schedule_id(schedule_type: ScheduleType, user_id: int, another_group_schedule_id: Optional[int] = None, dates: Optional[List[str]] = None) -> Tuple[Optional[Union[List[str], str]], Optional[str]]:
    is_own_group_asked: bool = another_group_schedule_id is None
    
    if is_own_group_asked:
        user: Any = (
            GroupsOfStudents.get_or_none(GroupsOfStudents.user_id == user_id) or
            CompactStudents.get_or_none(CompactStudents.user_id == user_id)
        )
        
        group_schedule_id: int = user.group_schedule_id
    else:
        group_schedule_id: int = another_group_schedule_id
    
    try:
        response: Dict[str, List[Dict[str, str]]] = get(url=SCHEDULE_URL, timeout=12, params={
            "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": schedule_type.value,
            "groupId": group_schedule_id
        }).json()
    except (ConnectionError, Timeout, JSONDecodeError):
        return (None, ResponseError.NO_RESPONSE)
    
    if not response:
        return (None, ResponseError.NO_DATA)
    
    settings: Settings = Settings.get(Settings.user_id == user_id)
    
    if schedule_type is ScheduleType.CLASSES:
        return (beautify_classes(raw_schedule=response, dates=dates, settings=settings), None)
    
    if schedule_type is ScheduleType.EXAMS:
        return (beautify_exams(raw_schedule=response, settings=settings), None)
    
    return(None, ResponseError.INCORRECT_SCHEDULE_TYPE)


def get_last_available_semester(user_id: int, is_card_check: bool = False) -> Tuple[Optional[int], Optional[ResponseError]]:
    student: BBStudents = BBStudents.get(BBStudents.user_id == user_id)
    
    # TODO: Implement score data fetching.
    #
    # try:
    #     page: str = post(SCORE_URL, timeout=12, data={
    #         "p_sub": P_SUB,
    #         "p_fac": student.institute_id,
    #         "p_kurs": student.year,
    #         "p_group": student.group_score_id,
    #         "p_stud": student.name_id,
    #         "p_zach": student.card.encode("CP1251")
    #     }).content.decode("CP1251")
        
    #     parsed_page: BeautifulSoup = BeautifulSoup(page, "html.parser")
    #     selector: Optional[Tag] = parsed_page.find(name="select", attrs={ "name": "semestr" })
        
    #     semesters: List[int] = map(lambda option: int(option["value"]), selector.find_all("option"))
    # except (ConnectionError, Timeout):
    #     return (None, ResponseError.NO_RESPONSE)
    # except (ValueError, KeyError):
    #     return (None, ResponseError.NO_DATA)
    # except AttributeError:
    #     return (None, ResponseError.INCORRECT_CARD if is_card_check else ResponseError.NO_DATA)
    # else:
    #     return (max(semesters), None)

def get_scoretable(semester: str, user_id: int) -> Tuple[Optional[List[Tuple[str, str]]], Optional[ResponseError]]:
    student: BBStudents = BBStudents.get(BBStudents.user_id == user_id)

    # TODO: Implement score data fetching.
    #
    # try:
    #     page: str = post(SCORE_URL, timeout=12, data={
    #         "p_sub": P_SUB,
    #         "p_fac": student.institute_id,
    #         "p_kurs": student.year,
    #         "p_group": student.group_score_id,
    #         "p_stud": student.name_id,
    #         "p_zach": student.card.encode("CP1251"),
    #         "semestr": semester
    #     }).content.decode("CP1251")
        
    #     parsed_page: BeautifulSoup = BeautifulSoup(page, features="html.parser")
    #     table: Tag = parsed_page.find(name="table", attrs={ "id": "reyt" })
        
    #     raw_scoretable: List[List[str]] = [ [
    #             (data.text if data.text else "-") for data in row.find_all("td")
    #         ] for row in table.find_all("tr")
    #     ][2:]
    # except (ConnectionError, Timeout):
    #     return (None, ResponseError.NO_RESPONSE)
    # except (AttributeError, ValueError, KeyError):
    #     return (None, ResponseError.NO_DATA)
    # else:
    #     return (beautify_scoretable(raw_scoretable=raw_scoretable), None)
