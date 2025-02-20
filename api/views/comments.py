from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from service_objects.services import ServiceOutcome

from drf_yasg.utils import swagger_auto_schema

from api.serializers.comments.retrieve import RetrieveCommentSerializer
from api.services.comments.create import CreateCommentService
from api.services.comments.delete import DeleteCommentService
from api.services.comments.list import ListCommentService
from api.services.comments.update import UpdatePatchCommentService, UpdatePutCommentService 


class ListCreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request: Request, *args, **kwagrs) -> Response:
        outcome = ServiceOutcome(ListCommentService, {'post_id': request.GET.get('post_id')})
        return Response(RetrieveCommentSerializer(outcome.result, many=True).data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(
            CreateCommentService, 
            request.data | {'author': request.user},
            request.FILES
        )
        return Response(RetrieveCommentSerializer(outcome.result).data, status=status.HTTP_201_CREATED)




class RetrieveUpdateDeleteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def patch(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(UpdatePatchCommentService, request.data | {'id': kwargs['pk']})
        return Response(RetrieveCommentSerializer(outcome.result).data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(UpdatePutCommentService, request.data | {'id': kwargs['pk']})
        return Response(RetrieveCommentSerializer(outcome.result).data, status=status.HTTP_200_OK)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(DeleteCommentService, {'post': kwargs['pk']})
        return Response(status=outcome.response_status)
        