from django.conf import settings
from django.urls import path

from graphqlapi.views import PrivateGraphQLView, TestGraphQLView

urlpatterns = [
    path('graphql/', PrivateGraphQLView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('graphqltest/', TestGraphQLView.as_view(graphiql=True)),
        path('graphqltest/<int:id>', TestGraphQLView.as_view(graphiql=True)),
    ]
