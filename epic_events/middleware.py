import logging


class EpicEventsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('file')

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code < 300:
            self.logger.info(f"{request.method} "
                             f"{request.path} "
                             f"{response.status_code}")
        elif response.status_code < 500:
            self.logger.warning(f"{request.method} "
                                f"{request.path} "
                                f"{response.status_code} "
                                f"{response.reason_phrase} "
                                f"{request.user} "
                                f"{request.environ['REMOTE_ADDR']}")
        else:
            self.logger.error(f"{request.method} "
                              f"{request.path} "
                              f"{response.status_code} "
                              f"{response.reason_phrase} "
                              f"{request.POST or request.GET} "                              
                              f"{request.user} "
                              f"{request.environ['REMOTE_ADDR']}")

        return response
