from rest_framework import status
from django.utils.functional import cached_property

from kfsdutils.apps.core.utils import ConfigUtils, DictUtils, HTTPUtils
from kfsdutils.apps.frontend.handlers.apiclient import APIClient

class TokenUser:
    is_active = True

    def __init__(self, request, token):
        self.__client = APIClient()
        self.__token = token
        self.__request = request
        self.__tokenPayload = self.genTokenPayload()
        if not self.__tokenPayload:
            raise Exception("Invalid token data found")

    def getConfigData(self):
        return self.getRequest().config.getFinalConfig()
    
    def getRequest(self):
        return self.__request
    
    def findConfigs(self, paths):
        return ConfigUtils.findConfigValues(
            self.getConfigData(),
            paths
        )
    
    def formatUrl(self, args):
        return "/".join(args)
    
    def getHttpHeaders(self):
        return {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.getRequest().COOKIES.get('csrftoken'),
            'Cookie': HTTPUtils.cookieToHeaderStr(self.getRequest(), ["access_token", "refresh_token", "csrftoken"])
        }

    def genTokenPayload(self):
        print("Request Path: {}, Method: {}".format(self.getRequest().path, self.getRequest().method))
        authHost, tokenDecodeUri = self.findConfigs(["auth_api.host", "auth_api.token_extract_url"])
        tokenPayloadUrl = self.formatUrl([authHost, tokenDecodeUri])
        payload = {
            "token": self.__token
        }
        headers = self.getHttpHeaders()
        resp_status, resp = self.__client.post(tokenPayloadUrl, status.HTTP_200_OK, APIClient.JSON, json=payload, headers=headers)
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
