from .check_local_user_enviroment import SudoPrivileges
from .first_run_setup import FirstRunSetup
from .nextcloud_activities import NextcloudActivities
from .nextcloud_file_operations import NextcloudFileOperations
from .nextcloud_talk_extractor import NextcloudTalkExtractor
from .nextcloud_user import NextcloudUser
from .nextcloud_meeting import NextcloudMeeting
from .nextcloud_poll import NextcloudPoll
from .nextcloud_requests import NextcloudRequests
from .nextcloud_data import NextcloudData
from .nextcloud_messages import NextcloudMessages
from .headers import NextcloudHeaders
from .translations import TRANSLATIONS
from .confirmation import are_you_sure
from .permissions_map import permissions_map
from .conversations_map import conversations_map


class NextcloudTalkBot:
    def __init__(self):
        pass
