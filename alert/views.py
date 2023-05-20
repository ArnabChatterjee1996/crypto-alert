from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view

from alert.constants import DELETED
from alert.exceptions import RequestValidationException
from alert.models import Alert
from alert.response import SuccessResponse, create_response, ValidationResponse, FailureResponse
from alert.serializers import CreateAlertSerializer, AlertSerializer
from alert.validations import validate_create_alert_request


@api_view(['POST'])
def create_alert(request):
    try:
        validate_create_alert_request(request, CreateAlertSerializer)
        alert, created = Alert.objects.get_or_create(
            user=User.objects.get_by_natural_key(request.data['user_name']),
            currency=request.data['currency'],
            limit=request.data['limit']
        )
        if not created:
            return create_response(FailureResponse("Entry with these details already exist",
                                                   status.HTTP_409_CONFLICT))
        return create_response(SuccessResponse({"alert_id": alert.pk}))
    except RequestValidationException as e:
        print(e.errors)
        return create_response(ValidationResponse(e.errors))
    except User.DoesNotExist:
        return create_response(
            FailureResponse("User with username : {} does not exist".format(request.data['user_name']),
                            status.HTTP_404_NOT_FOUND))
    except Exception as e:
        print("Exception occurred in creating alert : {}".format(e))
        return create_response(FailureResponse())


@api_view(['DELETE'])
def delete_alert(request, alert_id):
    try:
        alert = Alert.objects.get(pk=alert_id)
        if alert.status == DELETED:
            return create_response(FailureResponse("Alert with id : {} is already deleted".format(alert_id),
                                                   status.HTTP_409_CONFLICT))
        alert.status = DELETED
        alert.save()
        return create_response(SuccessResponse("Alert with id : {} deleted successfully".format(alert_id)))
    except Alert.DoesNotExist:
        return create_response(FailureResponse("Alert with id : {} does not exist".format(alert_id),
                                               status.HTTP_404_NOT_FOUND))
    except Exception as e:
        print("Exception occurred in deleting alert id : {} exception : {}".format(alert_id, e))
        return create_response(FailureResponse())


@api_view(['GET'])
def get_all_alerts_for_user(request, user_name):
    try:
        alert_status = None
        if 'status' in request.GET:
            alert_status = request.GET['status']
        if alert_status:
            alerts = Alert.objects.filter(user=User.objects.get_by_natural_key(username=user_name),
                                          status=alert_status)
        else:
            alerts = Alert.objects.filter(user=User.objects.get_by_natural_key(username=user_name))
        return create_response(SuccessResponse(data=alerts), AlertSerializer)
    except User.DoesNotExist:
        return create_response(FailureResponse("User with username : {} does not exist".format(user_name),
                                               status.HTTP_404_NOT_FOUND))
    except Exception as e:
        print("Exception occurred in getting alerts for username : {} , exception : {}".format(user_name, e))
        return create_response(FailureResponse())
