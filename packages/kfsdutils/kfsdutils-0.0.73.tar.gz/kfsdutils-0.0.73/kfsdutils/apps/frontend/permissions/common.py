from kfsdutils.apps.frontend.permissions.base import BasePermission
from kfsdutils.apps.frontend.exceptions import FEException
from kfsdutils.apps.core.utils import GeneralUtils
from http import HTTPStatus

class SignInRequired(BasePermission):
    def __init__(self, request):
        BasePermission.__init__(self, request)

    def __str__(self):
        return "Is authenticated check"

    def is_valid(self):
       if self.getUser().is_authenticated:
           return True
       return False
       
    def raise_exception(self):
        raise FEException(self.__str__(), HTTPStatus.TEMPORARY_REDIRECT, self.redirect_url())
    
    def redirect_url(self):
        loginUrl = self.constructUrl(self.getConfigPaths(["auth_fe.host", "auth_fe.login_url"]))
        loginUrl += "?next={}".format(GeneralUtils.genUrlEncode(self.getCurrentRequestUrl()))
        return loginUrl
    
    def redirect_url_neg(self):
        verifiedFinalUrl = self.constructUrl(self.getConfigPaths(["auth_fe.register_verify_success_url"]))
        return verifiedFinalUrl
    
    def raise_exception_neg(self):
        raise FEException(self.__str__(), HTTPStatus.TEMPORARY_REDIRECT, self.redirect_url_neg())
    

class SignUpEmailVerifiedStatusRequired(BasePermission):
    def __init__(self, request):
        BasePermission.__init__(self, request)

    def __str__(self):
        return "Is email verified check"

    def is_valid(self):
       if self.getUser().is_authenticated and self.getUser().is_email_verified():
           return True
       return False
       
    def raise_exception(self):
        raise FEException(self.__str__(), HTTPStatus.TEMPORARY_REDIRECT, self.redirect_url())
    
    def redirect_url(self):
        verifyEmailUrl = self.constructUrl(self.getConfigPaths(["auth_fe.host", "auth_fe.verify_email_url"]))
        verifyEmailUrl +="?next={}".format(GeneralUtils.genUrlEncode(self.getCurrentRequestUrl()))
        return verifyEmailUrl
    
    def redirect_url_neg(self):
        verifiedFinalUrl = self.constructUrl(self.getConfigPaths(["auth_fe.register_verify_success_url"]))
        return verifiedFinalUrl
    
    def raise_exception_neg(self):
        raise FEException(self.__str__(), HTTPStatus.TEMPORARY_REDIRECT, self.redirect_url_neg())