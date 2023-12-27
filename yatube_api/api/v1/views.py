from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, filters, generics, status
from rest_framework.response import Response

from api.v1.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Follow, Group, Post


User = get_user_model()


class BaseAuthorViewSet(viewsets.ModelViewSet):
    """Определение базовых параметров, для объектов имеющих поле автора."""

    def perform_create(self, serializer):
        fields = {
            'author': self.request.user,
        }

        if isinstance(self, CommentViewSet):
            fields['post'] = self.get_post_object()

        serializer.save(**fields)


class PostViewSet(BaseAuthorViewSet):
    """Представление для публикаций."""

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().select_related('group')


class CommentViewSet(BaseAuthorViewSet):
    """Представление для комментариев к публикациям."""

    serializer_class = CommentSerializer

    def get_post_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk_post'])

    def get_queryset(self):
        post = self.get_post_object()
        return post.comments.all()


class FollowViewSet(viewsets.GenericViewSet, generics.ListCreateAPIView):
    """Представление для подписок пользователей."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follows.all()

    def create(self, request, *args, **kwargs):
        data = {'user': request.user, 'following': ''}
        following = ''

        if 'following' in request.data:
            following = request.data['following']

        if following == '':
            return Response(
                {'following': 'Обязательное поле.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data['following'] = get_object_or_404(User, username=following)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class GroupViewSet(
    viewsets.GenericViewSet, generics.ListAPIView, generics.RetrieveAPIView
):
    """Представление для сообществ."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
