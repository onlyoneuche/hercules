from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 400:
            errors = []
            for field, error_list in response.data.items():
                for error in error_list:
                    errors.append({
                        "field": field,
                        "message": str(error)
                    })
            response.data = {"errors": errors}
            response.status_code = 422

    return response
