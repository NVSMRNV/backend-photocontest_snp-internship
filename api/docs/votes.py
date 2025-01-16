from drf_yasg import openapi
from api.serializers.votes.create import CreateVoteSerializer
from api.serializers.votes.retrieve import RetrieveVoteSerializer


CREATE_VOTE = {
    "tags": ["votes"],
    "operation_description": "Create new vote",
    "request_body": CreateVoteSerializer,
    "responses": {
        201: openapi.Response('Success', RetrieveVoteSerializer),
        400: openapi.Response('Bad request')
    },
}



DELETE_VOTE = {
    "tags": ["votes"],
    "operation_description": "Delete vote",
    "request_body": CreateVoteSerializer,
    "responses": {
        204: openapi.Response('Success'),
        404: openapi.Response('Not found')  
    },
}