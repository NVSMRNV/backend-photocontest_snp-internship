from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.comments import (
    CREATE_COMMENT,
    DELETE_COMMENT,
    RETRIEVE_COMMENT,
    UPDATE_COMMENT,
)
from api.serializers.comments.retrieve import RetrieveCommentSerializer
from api.services.comments.create import CreateCommentService
from api.services.comments.delete import DeleteCommentService
from api.services.comments.list import ListCommentService
from api.services.comments.update import (
    FullUpdateCommentService,
    PartialUpdateCommentService,
)


class ListCreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(**RETRIEVE_COMMENT)
    def get(self, request: Request, *args, **kwagrs) -> Response:
        outcome = ServiceOutcome(ListCommentService, {'post_id': request.GET.get('post_id')})
        return Response(RetrieveCommentSerializer(outcome.result, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**CREATE_COMMENT)
    def post(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(CreateCommentService, request.data | {'author_id': request.user.id},)
        return Response(RetrieveCommentSerializer(outcome.result).data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDeleteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**UPDATE_COMMENT)
    def patch(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(PartialUpdateCommentService, request.data | {'comment_id': kwargs['id']})
        return Response(RetrieveCommentSerializer(outcome.result).data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(**UPDATE_COMMENT)
    def put(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(FullUpdateCommentService, request.data | {'comment_id': kwargs['id']})
        return Response(RetrieveCommentSerializer(outcome.result).data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(**DELETE_COMMENT)       
    def delete(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(DeleteCommentService, {'comment_id': kwargs['id']})
        return Response(status=outcome.response_status)
        