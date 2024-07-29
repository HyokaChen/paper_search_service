from extra.core import PearApi
from api.views import router
n_api = PearApi()


# 统一处理server异常
@n_api.exception_handler(Exception)
def a(request, exc):

    if hasattr(exc, 'errno'):
        return n_api.create_response(request, data=[], msg=str(exc), code=exc.errno)
    else:
        return n_api.create_response(request, data=[], msg=str(exc), code=500)


n_api.add_router('/', router)

