from rest_framework import status
from django.utils.functional import cached_property

from kfsdutils.apps.core.utils import ConfigUtils, DictUtils
from kfsdutils.apps.frontend.handlers.apiclient import APIClient

class TokenUser:
    is_active = True

    def __init__(self, config, token):
        self.__client = APIClient()
        self.__token = token
        self.__config = config
        self.__tokenPayload = self.genTokenPayload()
        if not self.__tokenPayload:
            raise Exception("Invalid token data found")

    def getConfigData(self):
        return self.__config

    def genTokenPayload(self):
        authHost, tokenDecodeUri = ConfigUtils.findConfigValues(
            self.getConfigData(),
            ["auth_api.host", "auth_api.token_extract_url"]
        )
        url = "{authHost}/{tokenDecodeUri}".format(authHost=authHost, tokenDecodeUri=tokenDecodeUri)
        payload = {
            "token": self.__token
        }
        headers = {'Content-Type': 'application/json'}
        resp_status, resp = self.__client.post(url, status.HTTP_200_OK, APIClient.JSON, json=payload, headers=headers)
        if resp_status:
            return DictUtils.getDictValue(resp, "payload", {})

    def identifier(self):
        return DictUtils.getDictValue(self.__tokenPayload, "identifier")

    def username(self):
        return DictUtils.getDictValue(self.__tokenPayload, "email")

    def first_name(self):
        return DictUtils.getDictValue(self.__tokenPayload, "first_name")

    def last_name(self):
        return DictUtils.getDictValue(self.__tokenPayload, "last_name")

    def is_staff(self):
        return DictUtils.getDictValue(self.__tokenPayload, "is_staff", False)

    def is_superuser(self):
        return DictUtils.getDictValue(self.__tokenPayload, "is_superuser", False)
    
    def is_email_verified(self):
        return DictUtils.getDictValue(self.__tokenPayload, "is_email_verified", False)
    
    @cached_property
    def is_anonymous(self):
        return False

    @cached_property
    def is_authenticated(self):
        return True

    def get_username(self):
        return DictUtils.getDictValue(self.__tokenPayload, "email")

    def groups(self):
        # Not implemented
        return set()

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        return False

    def has_module_perms(self, module):
        return False
