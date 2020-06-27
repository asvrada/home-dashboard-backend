from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

from backend import models


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    raise_exception = True


class TestGraphQLView(GraphQLView):
    @property
    def username(self):
        return self.kwargs.get('username', None)

    def dispatch(self, request, *args, **kwargs):
        if self.username:
            users = models.User.objects.filter(username=self.username)
            if len(users) == 1:
                self.request.user = users.first()

        return super().dispatch(request, *args, **kwargs)
