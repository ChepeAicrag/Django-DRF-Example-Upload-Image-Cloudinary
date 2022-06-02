from drf_base64.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('user_permissions', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        image = validated_data.get('image', None)
        if not image is None:
            user.image = image
        user.save()
        return user

class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_staff', 'status_delete', 'is_active',
                   'is_superuser', 'password', 'user_permissions', 'groups')