from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post


User = get_user_model()


class BaseAuthorTextSerializer(serializers.ModelSerializer):
    """Базовый сериализатор, для моделей с полями текста и автора."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate_text(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError('Обязательное поле.')

        return value


class PostSerializer(BaseAuthorTextSerializer):
    """Сериализатор, для модели публикации."""

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор, для модели сообщества."""

    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(BaseAuthorTextSerializer):
    """Сериализатор, для модели комментария."""

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериaлизатор, для модели подписки."""

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def to_internal_value(self, data):
        if 'following' in data:
            if len(data['following'].strip()) > 0:
                following_user = get_object_or_404(
                    User, username=data['following']
                )
                return {'following': following_user}

        return {'following': None}

    def create(self, validated_data):
        user = validated_data['user']
        following = validated_data['following']

        if following is None:
            raise serializers.ValidationError(
                {'following': 'Обязательное поле'}
            )
        if user == following:
            raise serializers.ValidationError(
                {'details': 'Невозможно подписаться на самого себя.'}
            )

        follow_exist = Follow.objects.filter(
            user=user, following=following
        ).exists()

        if follow_exist:
            raise serializers.ValidationError(
                {'details': 'Подписка уже оформлена.'}
            )

        follow = Follow.objects.create(user=user, following=following)
        return follow
