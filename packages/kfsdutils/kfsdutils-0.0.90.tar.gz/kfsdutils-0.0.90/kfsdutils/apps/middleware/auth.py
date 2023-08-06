from kfsdutils.apps.frontend.handlers.login import LoginHandler


class KubefacetsAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        loginHandler = LoginHandler(request)
        loginHandler.preProcessRequest()

        request.user = loginHandler.getUser()
        response = self.get_response(request)

        loginHandler.postProcessResponse(response)
        return response