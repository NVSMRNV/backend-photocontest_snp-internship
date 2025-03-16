from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.posts import CREATE_POST, DELETE_POST, RETRIEVE_POST, UPDATE_POST
from api.permissions.isowner import IsOwner
from api.serializers.posts.retrieve import RetrievePostSerializer
from api.services.posts.create import CreatePostService
from api.services.posts.delete import DeletePostService
from api.services.posts.list import ListPostService
from api.services.posts.retrieve import RetrievePostService
from api.services.posts.update import (
    FullUpdatePostService,
    PartialUpdatePostService,
)


class ListCreatePostAPIView(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(**RETRIEVE_POST)
    def get(self, request: Request, *args, **kwagrs) -> Response:
        outcome = ServiceOutcome(ListPostService, request.data)
        return Response(RetrievePostSerializer(outcome.result, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**CREATE_POST)
    def post(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(CreatePostService, request.data.dict() | {'author': request.user.id}, request.FILES)
        return Response(RetrievePostSerializer(outcome.result).data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDeletePostAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(**RETRIEVE_POST)
    def get(self, request: Request, *args, **kwagrs) -> Response:
        outcome = ServiceOutcome(RetrievePostService, {'id': kwagrs['pk']})
        return Response(RetrievePostSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**UPDATE_POST)
    def patch(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(PartialUpdatePostService, request.data | {'id': kwargs['pk']})
        return Response(RetrievePostSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**UPDATE_POST)
    def put(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(FullUpdatePostService, request.data | {'id': kwargs['pk']})
        return Response(RetrievePostSerializer(outcome.result).data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(**DELETE_POST)
    def delete(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(DeletePostService, {'id': kwargs['pk']})
        return Response(status=outcome.response_status)
        