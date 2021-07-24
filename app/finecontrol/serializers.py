from rest_framework import serializers
from .models import Method_Db


class MethodSerializer(serializers.ModelSerializer):
    auth = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Method_Db
        fields = ['id', 'filename', 'auth']
        read_only_fields = ['id']
