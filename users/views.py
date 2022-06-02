from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .models import User
from .serializers import UserSerializer, UserListSerializer


class CrearListarUser(APIView):

    permission_classes = (AllowAny, )
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        users = User.objects.all().filter(status_delete=False)
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        file = request.data.get('image', None)
        request.data['image'] = file
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class ActualizarListarEliminarUserById(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, id):
        users = User.objects.all().filter(status_delete=False, id=id)
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, id):
        user = User.objects.filter(status_delete=False, id=id).first()
        if not user:
            return Response({'message': 'Usuario no encontrado'}, status=HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(
            data=request.data, instance=user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, id):
        user = User.objects.filter(status_delete=False, id=id).first()
        if not user:
            return Response({'message': 'Usuario no encontrado'}, status=HTTP_400_BAD_REQUEST)
        user.status_delete = True
        user.save()
        return Response({'message': 'Usuario eliminado satisfactoriamente'}, status=HTTP_200_OK)
