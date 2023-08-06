from kfsdutils.apps.core.utils import DictUtils

class BasePermission:
    def __init__(self, request):
        self.__request = request

    def getRequest(self):
        return self.__request
    
    def getConfigData(self):
        return self.__request.config.getFinalConfig()
    
    def getUser(self):
        return self.getRequest().user
    
    def getConfigValue(self, path):
        return DictUtils.getValueFromKeyPath(path, self.getConfigData())
    
    def constructUrl(self, paths):
        return "/".join(paths)
    
    def getConfigPaths(self, paths):
        return [ DictUtils.getValueFromKeyPath(path, self.getConfigData()) for path in paths]
    
    def getHttpHost(self):
        return self.getRequest().META.get('HTTP_HOST')
    
    def getHttpPath(self):
        return self.getRequest().META.get('PATH_INFO')
    
    def getRefererUrl(self):
        return self.getRequest().META.get('HTTP_REFERER')
    
    def getCurrentRequestUrl(self):
        return self.getRequest().build_absolute_uri()

    

    
