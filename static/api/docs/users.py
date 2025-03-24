from drf_yasg import openapi

from api.serializers.users.register import RegisterUserSerializer
from api.serializers.users.retrieve import RetrieveUserSerializer
from api.serializers.users.update import UpdateUserSerializer

REGISTER_USER = {
    "tags": ["users"],
    "operation_description": "Register new user",
    "request_body": RegisterUserSerializer,
    "responses": {
        201: openapi.Response('Success', RetrieveUserSerializer),
        400: openapi.Response('Bad request')
    },
}

RETRIEVE_USER = {
    "tags": ["users"],
    "operation_description": "Retrieve user by id",
    "responses": {
        200: openapi.Response('Success', RetrieveUserSerializer),
        404: openapi.Response('Not found')    
    },
}

UPDATE_USER = {
    "tags": ["users"],
    "operation_description": "Update user by id",
    "request_body": UpdateUserSerializer,
    "responses": {
        200: openapi.Response('Success', RetrieveUserSerializer),
        404: openapi.Response('Not found')    
    },
}

DELETE_USER = {
    "tags": ["users"],
    "operation_description": "Delete user by id",
    "responses": {
        200: openapi.Response('Success'),
        404: openapi.Response('Not found')  
    },
}
