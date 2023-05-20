from rest_framework import serializers

from alert.models import Alert


class CreateAlertSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100,allow_blank=False,allow_null=False)
    currency = serializers.CharField(max_length=10,allow_blank=False,allow_null=False)
    limit = serializers.DecimalField(max_digits=15,decimal_places=4,allow_null=False)

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id','user','currency','limit','status']