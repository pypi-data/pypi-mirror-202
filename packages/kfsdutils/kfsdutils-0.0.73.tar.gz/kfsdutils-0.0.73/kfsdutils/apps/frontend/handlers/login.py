from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from http import HTTPStatus

from kfsdutils.apps.core.utils import DictUtils, ConfigUtils, GeneralUtils
from kfsdutils.apps.frontend.handlers.apiclient import APIClient
from kfsdutils.apps.frontend.handlers.tokenuser import TokenUser


class LoginHandler:
    EXPIRY_IN_MINS = "expiry_in_mins"

    def __init__(self, request):
        self.__client = APIClient()
        self.__request = request
        self.__newAccessTokenResp = None

    def getRequest(self):
        return self.__request

    def getRuntimeConfig(self):
        if getattr(self.__request, "config"):
            return self.__request.config

    def getConfigData(self):
        return self.getRuntimeConfig().getFinalConfig()

    def getHttpHeaders(self):
        return {'Content-Type': 'application/json'}

    def httpGet(self, url, expStatus):
        return self.__client.get(
            url, expStatus, APIClient.JSON, headers=self.getHttpHeaders()
        )

    def httpPost(self, url, expStatus, payload):
        return self.__client.post(
            url, expStatus, APIClient.JSON, json=payload, headers=self.getHttpHeaders()
        )

    def formatUrl(self, args):
        return "/".join(args)

    def findConfigs(self, paths):
        return ConfigUtils.findConfigValues(
            self.getConfigData(),
            paths
        )
    
    def getRegisterSuccessUrl(self):
        registerVerifySuccessUri = self.findConfigs(["auth_fe.register_verify_success_url"])[0]
        return registerVerifySuccessUri

    def getVerifyTempTokens(self, code):
        authHost, verifyTokensUri = self.findConfigs(["auth_api.host", "auth_api.verify_tmp_tokens_url"])
        verifyTokensUri = verifyTokensUri.format(code)
        verifyTokensUrl = self.formatUrl([authHost, verifyTokensUri])
        return self.httpGet(verifyTokensUrl, HTTPStatus.OK)

    def sendVerifyEmail(self, email, emailType):
        authHost, verifyEmailUri, userIdentifierPrefix = self.findConfigs(["auth_api.host", "auth_api.verify_email_url", "auth_api.user_identifier_prefix"])
        userIdentifier = userIdentifierPrefix.format(email)
        payload = {"user": userIdentifier, "type": emailType}
        verifyEmailUrl = self.formatUrl([authHost, verifyEmailUri])
        return self.httpPost(verifyEmailUrl, [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST], payload)

    def genUserTokens(self, username):
        authHost, userTokensUriRaw, userIdentifierPrefix = self.findConfigs(["auth_api.host", "auth_api.user_tokens_url", "auth_api.user_identifier_prefix"])
        userIdentifier = userIdentifierPrefix.format(username)
        userTokensUri = userTokensUriRaw.format(GeneralUtils.genUrlEncode(userIdentifier))
        userTokensUrl = self.formatUrl([authHost, userTokensUri])
        return self.httpGet(userTokensUrl, status.HTTP_200_OK)

    def preProcessRequest(self):
        accessTokenFromCookie = self.getAccessTokenFromCookie()
        refreshTokenFromCookie = self.getRefreshTokenFromCookie()
        if not accessTokenFromCookie and refreshTokenFromCookie:
            self.__newAccessTokenResp = self.refreshAccessToken(refreshTokenFromCookie)
            if self.__newAccessTokenResp:
                self.getRequest().COOKIES[self.getAccessTokenCookieKey()] = DictUtils.getDictValue(self.__newAccessTokenResp, "token")

    def postProcessResponse(self, response):
        if self.__newAccessTokenResp:
            self.setAccessCookieInResponse(response, self.__newAccessTokenResp)

    def getLoggedInUser(self, accessTokenFromCookie):
        try:
            return TokenUser(self.getConfigData(), accessTokenFromCookie)
        except Exception:
            return AnonymousUser()

    def getUser(self):
        accessTokenFromCookie = self.getAccessTokenFromCookie()
        if not accessTokenFromCookie:
            return AnonymousUser()
        else:
            return self.getLoggedInUser(accessTokenFromCookie)

    def authenticate(self, username, password):
        data = {"username": username, "password": password}
        authHost, userLoginUrl = self.findConfigs(["auth_api.host", "auth_api.user_login_url"])
        loginUrl = self.formatUrl([authHost, userLoginUrl])
        resp_status, resp = self.httpPost(loginUrl, HTTPStatus.OK, data)

        if resp_status:
            return self.genUserTokens(username)

        return resp_status, resp

    def register(self, **kwargs):
        username = DictUtils.getDictValue(kwargs, "email")
        data = {
            "email": username,
            "password": DictUtils.getDictValue(kwargs, "password")
        }
        authHost, userRegisterUrl = self.findConfigs(["auth_api.host", "auth_api.user_register_url"])
        registerUrl = self.formatUrl([authHost, userRegisterUrl])
        resp_status, resp = self.httpPost(registerUrl, HTTPStatus.CREATED, data)
        return resp_status, resp

    def refreshAccessToken(self, refreshToken):
        if not refreshToken:
            return None, None

        authHost, refreshAccessTokenUri = self.findConfigs(["auth_api.host", "auth_api.access_token_refresh_url"])
        refreshAccessTokenUrl = self.formatUrl([authHost, refreshAccessTokenUri])
        payload = {"refresh_token": refreshToken}
        resp_status, resp = self.httpPost(refreshAccessTokenUrl, HTTPStatus.OK, payload)

        if resp_status:
            return resp
        return None

    def getAccessTokenCookieKey(self):
        return DictUtils.getValueFromKeyPath("cookie.access.key", self.getConfigData())

    def getRefreshTokenCookieKey(self):
        return DictUtils.getValueFromKeyPath("cookie.refresh.key", self.getConfigData())

    def getRememberMeCookieKey(self):
        return DictUtils.getValueFromKeyPath("cookie.remember_me.key", self.getConfigData())

    def getRememberMeFromCookie(self):
        return self.getRequest().COOKIES.get(self.getRememberMeCookieKey())

    def getAccessTokenFromCookie(self):
        return self.getRequest().COOKIES.get(self.getAccessTokenCookieKey())

    def getRefreshTokenFromCookie(self):
        return self.getRequest().COOKIES.get(self.getRefreshTokenCookieKey())

    def processTokenResp(self, token):
        tokenType = DictUtils.getDictValue(token, "type")
        expiryConfig = DictUtils.createDictTreeByKeysAndValueEdge(
            ["cookie", tokenType],
            {self.EXPIRY_IN_MINS: DictUtils.getDictValue(token, self.EXPIRY_IN_MINS)}
        )
        settingConfigPath = "cookie.{}".format(tokenType)
        cookieConfig = DictUtils.mergeDicts(
            self.getConfigData(),
            expiryConfig
        )
        tokenVal = DictUtils.getDictValue(token, "token")
        return DictUtils.getValueFromKeyPath(settingConfigPath, cookieConfig), tokenVal

    def setRememberMeCookie(self, response, rememberMe):
        self.setCookie(
            response,
            DictUtils.getValueFromKeyPath("cookie.remember_me", self.getConfigData()),
            rememberMe,
            False if rememberMe else True
        )

    def setLoginCookies(self, response, loginTokens, rememberMe):
        for token in loginTokens:
            cookieConfig, tokenVal = self.processTokenResp(token)
            self.setCookie(
                response,
                cookieConfig,
                tokenVal
            )

        self.setRememberMeCookie(response, rememberMe)

    def unsetLoginCookies(self, response):
        for cookieName in ["refresh", "access"]:
            configPath = "cookie.{}".format(cookieName)
            self.setCookie(
                response,
                DictUtils.getValueFromKeyPath(configPath, self.getConfigData()),
                None,
                True
            )

    def setAccessCookieInResponse(self, response, tokenResp):
        cookieConfig, tokenVal = self.processTokenResp(tokenResp)
        self.setCookie(
            response,
            cookieConfig,
            tokenVal
        )

    def setCookie(self, response, config, cookie, unset=False):
        if not unset:
            response.set_cookie(
                key=config['key'],
                value=cookie,
                expires=config['expiry_in_mins']*60,
                secure=config['secure'],
                httponly=config['http_only'],
                samesite=config['same_site']
            )
        else:
            response.delete_cookie(
                key=config['key']
            )
