from service_objects.services import ServiceWithResult

from models.models.posts.models import Post


class ListPostService(ServiceWithResult):
    def process(self) -> ServiceWithResult:
        self.result = Post.objects.all()
        return self
