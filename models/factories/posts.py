import factory
from faker import Faker

from models.models.posts.models import Post

faker = Faker()

class PostFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory('models.factories.users.UserFactory')
    image = factory.django.ImageField()
    title = faker.word()
    description = faker.text()
    status = 'APPROVED'
    
    class Meta:
        model = Post