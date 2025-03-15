import factory
from faker import Faker

from models.models.posts.models import User

faker = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f'{faker.user_name()}_{n}')

    class Meta:
        model = User