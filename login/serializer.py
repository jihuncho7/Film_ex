from rest_framework import serializers

from login.models import User


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_2 = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'social','username','email','image','phone'
                  )
        read_only_fields = ('email','id','social')
