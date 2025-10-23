from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.controllers.analyze_controller import AnalyzeController

class AnalyzeView:
    def __init__(self):
        self.controller = AnalyzeController()

    def enqueue(self, http_request: HttpRequest) -> HttpResponse:
        formatted_response = self.controller.enqueue(http_request)

        return HttpResponse(status_code=202, body={
            "status": True,
            "message": "Job queued successfully",
            "data": formatted_response,
        })

    def get_status(self, http_request: HttpRequest) -> HttpResponse:
        formatted_response = self.controller.get_status(http_request)

        return HttpResponse(status_code=200, body={
            "status": True,
            "message": "Job status retrieved successfully",
            "data": formatted_response,
        })
    