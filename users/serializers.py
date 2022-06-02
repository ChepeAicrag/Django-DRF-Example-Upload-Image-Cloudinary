from django.conf import settings
from drf_base64.serializers import ModelSerializer
import cloudinary

from .models import User

class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_staff', 'status_delete', 'is_active',
                   'is_superuser', 'password', 'user_permissions', 'groups')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop("image")
        response.setdefault('image', instance.image.public_id)
        return response

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
            upload_data = cloudinary.uploader.upload(
                image, folder=f'media/users/{validated_data.get("email")}/')
            user.image = upload_data['secure_url']
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        validated_data.pop('email', None)
        image = validated_data.get('image', None)
        if not image is None:
            if instance.image == 'https://res.cloudinary.com/instituto-tecnol-gico-de-oaxaca/v1654150473/default_fltufw.webp':    
                upload_data = cloudinary.uploader.upload(
                    image, folder=f'media/users/{instance.email}/')
                validated_data['image'] = upload_data['secure_url']
            else:
                print(instance.image)
                upload_data = cloudinary.uploader.upload(
                    image, public_id=f'media/users/{instance.email}/{str(instance.image).split("/")[-1]}')
                validated_data['image'] = upload_data['secure_url']            
        return super().update(instance, validated_data)
        

