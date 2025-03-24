from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.votes import CREATE_VOTE, DELETE_VOTE
from api.serializers.votes.retrieve import RetrieveVoteSerializer
from api.services.votes.create import CreateVoteService
from api.services.votes.delete import DeleteVoteService


class CreateDeleteVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**CREATE_VOTE)
    def post(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(
            CreateVoteService,
            {
                'user_id': request.user.id,
                'post_id': request.data['post_id'],
            },
        )
        return Response(RetrieveVoteSerializer(outcome.result).data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(**DELETE_VOTE)
    def delete(self, request: Request, *args, **kwargs) -> Response:
        outcome = ServiceOutcome(
            DeleteVoteService,             
            {
                'user_id': request.user.id,
                'post_id': request.data['post_id'],
            },
        )
        return Response(status=outcome.response_status)
