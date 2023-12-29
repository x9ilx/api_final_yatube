from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, filters, generics

from api.v1.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Group, Post


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Представление для публикаций."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментариев к публикациям."""

    serializer_class = CommentSerializer

    def get_post_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk_post'])

    def get_queryset(self):
        post = self.get_post_object()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post_object()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.GenericViewSet, generics.ListCreateAPIView):
    """Представление для подписок пользователей."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follows.all()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для сообществ."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
