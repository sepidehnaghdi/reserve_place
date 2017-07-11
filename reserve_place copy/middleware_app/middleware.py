from django.http import HttpResponse

class LoggingMiddleware(object):
    def __init__(self, get_response):
        print("here in init")
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        """Handle new-style middleware here."""
        response = self.process_request(request)

        if response is None:
            # If process_request returned None, we must call the next middleware or
            # the view. Note that here, we are sure that self.get_response is not
            # None because this method is executed only in new-style middlewares.
            try:
                response = self.get_response(request)
            except Exception as e:
                print("error")

        response = self.process_response(request, response)

        return response


    def process_request(self, request):
        pass
        # print(request.method)
        # # print(request.user)
        # print(request.get_host())
        # print(request)

    def process_response(self, request, response):
        # print("in process response")
        # print(response.content)
        # print(response.status_code)
        # print(response.reason_phrase)
        # import traceback
        # print(traceback.format_exc())
        return response

    def process_exception(self, request, exception):
        import traceback
        print(traceback.format_exc())
    # def process_view(request, view_func, view_args, view_kwargs):
    #     print("in proces view")
    #     print(request, view_func)
    #     return None

    # def process_exception(request, exception):
    #     print("in exception")

    # def process_template_response(request, response):
    #     print("in process_template_response")




