from typing import Optional
from typing import Union
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from json.decoder import JSONDecodeError

from requests import get
from requests import post
from requests import Response
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

from bs4 import BeautifulSoup
from bs4 import Tag

from bot.models.user import User
from bot.models.settings import Settings

from bot.utilities.api.helpers.schedule import beautify_classes
from bot.utilities.api.helpers.schedule import beautify_exams
from bot.utilities.api.constants import SCHEDULE_URL
from bot.utilities.api.constants import CAS_LOGIN_URL
from bot.utilities.api.constants import CAS_SERVICE_LOGIN_URL
from bot.utilities.api.constants import STUDENT_DATA_URL
from bot.utilities.api.constants import AUTH_TOKEN_SIGN
from bot.utilities.api.constants import AUTH_TOKEN_LENGTH
from bot.utilities.api.constants import SCORE_TEMPLATE
from bot.utilities.api.types import ResponseError
from bot.utilities.api.types import KaiRuDataType
from bot.utilities.api.types import ScheduleType


def get_group_schedule_id(group: str) -> Tuple[Optional[str], Optional[ResponseError]]:
    try:
        groups_json_list: List[Dict[str, str]] = get(url=SCHEDULE_URL, timeout=12, params={
            "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "getGroupsURL",
            "query": group
        }).json()
    except (ConnectionError, Timeout, JSONDecodeError):
        return (None, ResponseError.NO_RESPONSE)
    
    if len(groups_json_list) != 1 or "id" not in groups_json_list[0]:
        return (None, ResponseError.NO_DATA)
    
    return (groups_json_list[0]["id"], None)

def get_schedule_by_group_schedule_id(schedule_type: ScheduleType, user_id: int, another_group_schedule_id: Optional[int] = None, dates: Optional[List[str]] = None) -> Tuple[Optional[Union[List[str], str]], Optional[str]]:
    is_own_group_asked: bool = another_group_schedule_id is None
    group_schedule_id: int = User.get_or_none(User.user_id == user_id).group_schedule_id if is_own_group_asked else another_group_schedule_id
    
    try:
        schedule_json_list: Dict[str, List[Dict[str, str]]] = get(url=SCHEDULE_URL, timeout=12, params={
            "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": schedule_type.value,
            "groupId": group_schedule_id
        }).json()
    except (ConnectionError, Timeout, JSONDecodeError):
        return (None, ResponseError.NO_RESPONSE)
    
    if len(schedule_json_list) == 0:
        return (None, ResponseError.NO_DATA)
    
    settings: Settings = Settings.get(Settings.user_id == user_id)
    
    if schedule_type is ScheduleType.CLASSES:
        return (beautify_classes(raw_schedule=schedule_json_list, dates=dates, settings=settings), None)
    if schedule_type is ScheduleType.EXAMS:
        return (beautify_exams(raw_schedule=schedule_json_list, settings=settings), None)
    
    return(None, ResponseError.INCORRECT_SCHEDULE_TYPE)


def authenticate_user_via_kai_cas(user: User) -> Tuple[Optional[str], Optional[ResponseError]]:
    try:
        login_page_response: Response = get(url=CAS_LOGIN_URL, timeout=12)

        cas_login_page: str = login_page_response.text
        parsed_cas_login_page: BeautifulSoup = BeautifulSoup(cas_login_page, features="html.parser")
        input_for_token_LT: Tag = parsed_cas_login_page.find(name="input", attrs={ "name": "lt" })

        token_LT: str = input_for_token_LT["value"]
        token_JSESSIONID: str = login_page_response.cookies["JSESSIONID"]
    except (ConnectionError, Timeout):
        return (None, ResponseError.NO_RESPONSE)
    except KeyError:
        return (None, ResponseError.NO_DATA)

    try:
        cas_authentication_data_response: Response = post(
            url=CAS_LOGIN_URL,
            timeout=12,
            data={
                "username": user.bb_login,
                "password": user.bb_password,
                "execution": "e1s1",
                "_eventId": "submit",
                "lt": token_LT
            },
            headers={
                "Cookie": f"JSESSIONID={token_JSESSIONID}"
            }
        )

        token_CASTGC: str = cas_authentication_data_response.cookies["CASTGC"]
    except (ConnectionError, Timeout):
        return (None, ResponseError.NO_RESPONSE)
    except KeyError:
        return (None, ResponseError.INCORRECT_BB_CREDENTIALS)
    
    return (token_CASTGC, None)

def authorise_user_via_kai_cas(user: User) -> Tuple[Optional[str], Optional[ResponseError]]:
    (token_CASTGC, response_error) = authenticate_user_via_kai_cas(user=user)

    if token_CASTGC is None:
        return (None, response_error)
    
    try:
        cas_authorisation_data_response: Response = get(
            url=CAS_SERVICE_LOGIN_URL,
            timeout=12,
            headers={
                "Cookie": f"CASTGC={token_CASTGC}"
            }
        )
        
        token_JSESSIONID: str = cas_authorisation_data_response.history[1].cookies["JSESSIONID"]
    except (ConnectionError, Timeout):
        return (None, ResponseError.NO_RESPONSE)
    except (IndexError, KeyError):
        return (None, ResponseError.NO_DATA)
    
    return (token_JSESSIONID, None)

def get_score_data(user: User, semester: Optional[int] = None, auth_token: Optional[str] = None) -> Tuple[Optional[Tuple[str, List[str], List[Tuple[str, str]]]], Optional[ResponseError]]:
    (token_JSESSIONID, response_error) = authorise_user_via_kai_cas(user=user)

    if token_JSESSIONID is None:
        return (None, response_error)

    if (auth_token is None) != (semester is None):
        return (None, ResponseError.INCORRECT_SCORE_DATA)

    try:
        score_data_page: str = get(
            url=STUDENT_DATA_URL.format(data_type=KaiRuDataType.SCORE.value),
            timeout=12,
            params={} if auth_token is None else {
                "p_auth": auth_token,
                "p_p_id": "myBRS_WAR_myBRS10",
                "p_p_lifecycle": "1",
                "p_p_state": "normal",
                "p_p_mode": "view",
                "p_p_col_id": "column-2",
                "p_p_col_count": "1",
                "_myBRS_WAR_myBRS10_javax.portlet.action": "selectSemester",
                "semester": semester
            },
            headers={
                "Cookie": f"JSESSIONID={token_JSESSIONID}"
            }
        ).content.decode("utf-8")

        parsed_score_data_page: BeautifulSoup = BeautifulSoup(score_data_page, "html.parser")
        
        semester_selector: Optional[Tag] = parsed_score_data_page.find(name="select", attrs={ "name": "_myBRS_WAR_myBRS10_semester_0" })
        semesters: List[str] = [ option["value"] for option in semester_selector.find_all("option") ]

        score_table: Optional[Tag] = parsed_score_data_page.find(name="table", attrs={ "class": "table table-striped table-bordered" })
        score_data: List[List[str]] = [ [
                data.text for data in row.find_all("td")
            ] for row in score_table.find_all("tr")
        ][2:]
    except (ConnectionError, Timeout):
        return (None, ResponseError.NO_RESPONSE)
    except AttributeError:
        return (None, ResponseError.NO_DATA)

    # Slightly refining traditional assessment to be written starting with lower case letter
    for (subject_index, subject_score_data) in enumerate(score_data):
        score_data[subject_index][16] = subject_score_data[16].lower()
    
    score: List[Tuple[str, str]] = [
        (subject_score_data[1], SCORE_TEMPLATE.format(*subject_score_data[1:])) 
        for subject_score_data in score_data
    ]

    auth_token_start_index: int = score_data_page.find(AUTH_TOKEN_SIGN) + len(AUTH_TOKEN_SIGN)
    auth_token_end_index: int = auth_token_start_index + AUTH_TOKEN_LENGTH

    auth_token = score_data_page[auth_token_start_index:auth_token_end_index]

    return ((auth_token, semesters, score), None)
