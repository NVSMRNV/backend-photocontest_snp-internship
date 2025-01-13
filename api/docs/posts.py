from drf_yasg import openapi

from api.serializers.posts.create import CreatePostSerializer
from api.serializers.posts.retrieve import RetrievePostSerializer
from api.serializers.posts.update import UpdatePostSerializer


CREATE_POST = {
    "tags": ["posts"],
    "operation_description": "Create new post",
    "request_body": CreatePostSerializer,
    "responses": {
        201: openapi.Response('Success', RetrievePostSerializer),
        400: openapi.Response('Bad request')
    },
}

RETRIEVE_POST = {
    "tags": ["posts"],
    "operation_description": "Retrieve post by id",
    "responses": {
        200: openapi.Response('Success', RetrievePostSerializer),
        404: openapi.Response('Not found')    
    },
}

UPDATE_POST = {
    "tags": ["posts"],
    "operation_description": "Update post by id",
    "request_body": UpdatePostSerializer,
    "responses": {
        200: openapi.Response('Success', RetrievePostSerializer),
        404: openapi.Response('Not found')    
    },
}

DELETE_POST = {
    "tags": ["posts"],
    "operation_description": "Delete post by id",
    "responses": {
        204: openapi.Response('Success'),
        404: openapi.Response('Not found')  
    },
}
