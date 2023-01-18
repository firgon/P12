# import logging
#
# from rest_framework.views import exception_handler
#
#
# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)
#
#
#     # Now add the HTTP status code to the response.
#     if response is not None:
#         logger = logging.getLogger(__name__)
#
#         print("WARNING")
#         logger.warning(exc)
#         print("/WARNING")
#         # response.data['status_code'] = response.status_code
#     else:
#         print("exception handler but no answer", exc)
#
#     return response
