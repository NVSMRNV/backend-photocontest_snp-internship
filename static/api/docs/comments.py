from drf_yasg import openapi

from api.serializers.comments.create import CreateCommentSerializer
from api.serializers.comments.retrieve import RetrieveCommentSerializer
from api.serializers.comments.update import UpdateCommentSerializer


CREATE_COMMENT = {
    "tags": ["comments"],
    "operation_description": "Create new comment",
    "request_body": CreateCommentSerializer,
    "responses": {
        201: openapi.Response('Success', RetrieveCommentSerializer),
        404: openapi.Response('Not found')    
    },
}

RETRIEVE_COMMENT = {
    "tags": ["comments"],
    "operation_description": "Retrieve comment by id",
    "responses": {
        200: openapi.Response('Success', RetrieveCommentSerializer),
        404: openapi.Response('Not found')    
    },
}

UPDATE_COMMENT = {
    "tags": ["comments"],
    "operation_description": "Update comment by id",
    "request_body": UpdateCommentSerializer,
    "responses": {
        200: openapi.Response('Success', RetrieveCommentSerializer),
        404: openapi.Response('Not found')    
    },
}

DELETE_COMMENT = {
    "tags": ["comments"],
    "operation_description": "Delete comment by id",
    "responses": {
        200: openapi.Response('Success'),
        404: openapi.Response('Not found')  
    },
}
