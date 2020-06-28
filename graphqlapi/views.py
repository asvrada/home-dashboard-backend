from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

from backend import models


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    raise_exception = True


class TestGraphQLView(GraphQLView):
    @property
    def id(self):
        return self.kwargs.get('id', None)

    def dispatch(self, request, *args, **kwargs):
        if self.id:
            user = models.User.objects.get(pk=self.id)
            if user:
                self.request.user = user

        return super().dispatch(request, *args, **kwargs)
