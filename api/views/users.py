from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from service_objects.services import ServiceOutcome

from drf_yasg.utils import swagger_auto_schema 
from api.docs.users import (
    DELETE_USER,
    REGISTER_USER,
    RETRIEVE_USER,
    UPDATE_USER,
)

from api.serializers.users.retrieve import RetrieveUserSerializer
from api.services.users.delete import DeleteUserService
from api.services.users.retrieve import RetrieveUserService
from api.services.users.register import RegisterUserService
from api.services.users.update import (
    UpdatePatchUserService,
    UpdatePutUserService,
)


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**REGISTER_USER)
    def post(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(RegisterUserService, request.data)
        return Response(RetrieveUserSerializer(outcome.result).data, status=status.HTTP_201_CREATED)
    

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**RETRIEVE_USER)
    def get(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(RetrieveUserService, {'id': request.user.id})
        return Response(RetrieveUserSerializer(outcome.result).data, status=status.HTTP_200_OK)
    

class RetrieveUpdateDeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**RETRIEVE_USER)
    def get(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(RetrieveUserService, {'id': kwargs['pk']})
        return Response(RetrieveUserSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**UPDATE_USER)
    def put(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(UpdatePutUserService, request.data | {'id': kwargs['pk']})
        return Response(RetrieveUserSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**UPDATE_USER)
    def patch(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(UpdatePatchUserService, request.data | {'id': kwargs['pk']})
        return Response(RetrieveUserSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**DELETE_USER)
    def delete(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(DeleteUserService, {'id': kwargs['pk']})
        return Response(status=outcome.response_status)
