import json

from rest_framework.response import Response
from rest_framework import status

from alert.constants import SUCCESS, FAILURE


class BaseResponse:
    def __init__(self, status,status_code):
        self.status = status
        self.status_code = status_code

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    def get_status(self):
        return self.status_code


class SuccessResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(SUCCESS,status.HTTP_200_OK)
        self.data = data

class ValidationResponse(BaseResponse):
    def __init__(self, errors):
        super().__init__(FAILURE,status.HTTP_400_BAD_REQUEST)
        self.errors = errors



class FailureResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(FAILURE,status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.data = data

class FailureResponse(BaseResponse):
    def __init__(self, data=None, status_code=None):
        if data and status_code:
            super().__init__(FAILURE,status_code)
            self.data = data
        else:
            super().__init__(FAILURE, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.data = "Internal Error, check with developers"




def create_response(response,serializer=None):
    if serializer:
        serializer = serializer(response.data,many=True)
        print(serializer.data)
        return Response(serializer.data,response.get_status())
    return Response(response.toJson(),
                    status=response.get_status())
