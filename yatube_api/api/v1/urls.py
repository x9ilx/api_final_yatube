from django.urls import path, include
from rest_framework import routers

from api.v1.views import (
    CommentViewSet,
    FollowViewSet,
    GroupViewSet,
    PostViewSet,
)


router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='Post')
router.register('groups', GroupViewSet, basename='Group')
router.register(
    r'posts/(?P<pk_post>[^d]+)/comments', CommentViewSet, basename='Comment'
)
router.register('follow', FollowViewSet, basename='Follow')

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
