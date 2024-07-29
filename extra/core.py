from typing import Any, Optional
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI


class PearApi(NinjaAPI):
    def create_response(
        self,
        request: HttpRequest,
        data: Any,
        *,
        code: int = 2000,
        status: Optional[int] = None,
        msg: str = "Success",
        temporal_response: Optional[HttpResponse] = None,
    ) -> HttpResponse:
        std_data = {
            "code": code,
            "result": data,
            "message": msg,
            "success": True
        }
        content = self.renderer.render(request, std_data, response_status=status)
        content_type = "{}; charset={}".format(
            self.renderer.media_type, self.renderer.charset
        )

        return HttpResponse(content, status=status, content_type=content_type)


