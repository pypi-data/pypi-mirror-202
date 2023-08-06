from kfsdutils.apps.core.utils import HTTPUtils
from kfsdutils.apps.endpoints.exceptions import KubefacetsAPIException


def handle_http_exception(f):
    def wrapper(*args, **kwargs):
        try:
            expRespType, resp = f(*args, **kwargs)
            response = resp.json() if expRespType == APIClient.JSON else resp.text
            return True, response
        except KubefacetsAPIException as e:
            return False, {"detail": e.detail, "code": e.default_code}
        except Exception:
            return False, {"detail": "Unexpected error occurred, Please try again later.", "code": "unexpected_error"}

    return wrapper


class APIClient:
    JSON = "JSON"
    TEXT = "TEXT"

    def __init__(self):
        pass

    @handle_http_exception
    def post(self, url, expStatus, expRespType, **kwargs):
        resp = HTTPUtils.post(url, expStatus, **kwargs)
        return expRespType, resp

    @handle_http_exception
    def get(self, url, expStatus, expRespType, **kwargs):
        resp = HTTPUtils.get(url, expStatus, **kwargs)
        return expRespType, resp
