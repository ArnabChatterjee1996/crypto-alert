from alert.exceptions import RequestValidationException


def validate_create_alert_request(request,serializer):
    validation = serializer(data=request.data)
    if not validation.is_valid():
        raise RequestValidationException(validation.errors)
