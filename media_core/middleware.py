import logging
import time

logger = logging.getLogger(__name__)

class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        # Log request details
        logger.info(
            f"Request: {request.method} {request.path} "
            f"User: {request.user if request.user.is_authenticated else 'Anonymous'}"
        )
        print("inside middleware")
        response = self.get_response(request)

        duration = (time.time() - start_time) * 1000  # ms
        # Log response details
        logger.info(
            f"Response: {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration:.2f}ms"
        )

        return response