from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer


class Login(APIView):
    def post(self, request, format=None):
        phone = request.data.get('phone')
        password = request.data.get('password')

        user = authenticate(request, phone=phone, password=password)
        if not user:
            return Response(
                {'msg': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'name': user.name,
                'phone': str(user.phone),
                'jwt_token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )


class Profile(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_user(self, request):
        try:
            user, _ = JWTAuthentication().authenticate(request)
            return user
        except Exception as e:
            raise Http404

    def get(self, request, format=None):
        user = self.get_user(request)
        serializer = UserSerializer(user)

        user = modify_outgoing_data(serializer.data)
        return Response(user, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        user = self.get_user(request)
        serializer = UserSerializer(
            user,
            data=modify_incoming_data(request.data),
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'OK'}, status=status.HTTP_200_OK)
        return Response({'err': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def modify_incoming_data(data):
    if data.get('current_location'):
        data['lat'] = data['current_location']['lat']
        data['lng'] = data['current_location']['lng']
    return data


def modify_outgoing_data(data):
    data['current_location'] = {
        'lat': data.get('lat'),
        'lng': data.get('lng')
    }
    if data['lat']: del data['lat']
    if data['lng']: del data['lng']
    return data