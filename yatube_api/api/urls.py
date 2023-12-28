from django.urls import path, include
from rest_framework import routers

from api.v1.views import (
    CommentViewSet,
    FollowViewSet,
    GroupViewSet,
    PostViewSet,
)


v1_router = routers.DefaultRouter()
v1_router.register('posts', PostViewSet, basename='Post')
v1_router.register('groups', GroupViewSet, basename='Group')
v1_router.register(
    r'posts/(?P<pk_post>[^d]+)/comments', CommentViewSet, basename='Comment'
)
v1_router.register('follow', FollowViewSet, basename='Follow')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(v1_router.urls)),
]
