from .check_local_user_enviroment import check_user_and_abort_if_root_or_sudo
from .first_run_setup import FirstRunSetup
from .nextcloud_activities import NextcloudActivities
from .nextcloud_file_operations import NextcloudFileOperations
from .nextcloud_talk_extractor import NextcloudTalkExtractor
from .nextcloud_user import NextcloudUser
from .nextcloud_meeting import NextcloudMeeting
from .nextcloud_poll import NextcloudPoll
from .nextcloud_requests import NextcloudRequests
from .read_data import read_nextcloud_data
from .headers import create_headers
from .send_message import send_message_to_nextcloud_talk_group
from .translations import TRANSLATIONS
from .confirmation import are_you_sure
from.permissions_map import permissions_map
from .conversations_map import conversations_map


class NextcloudTalkBot:
    def __init__(self):
        pass
