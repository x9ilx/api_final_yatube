from django.contrib.auth import get_user_model
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
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Подписка уже оформлена',
            )
        ]

    def validate(self, attrs):
        if attrs['user'] == attrs['following']:
            raise serializers.ValidationError(
                {'details': 'Невозможно подписаться на самого себя.'}
            )
        return super().validate(attrs)
