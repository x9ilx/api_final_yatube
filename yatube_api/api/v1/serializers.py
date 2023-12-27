from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post


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
        fields = (
            'user',
            'following',
        )
        model = Follow

    def validate(self, attrs):
        user = self.initial_data['user']
        following = self.initial_data['following']

        if user == following:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя.'
            )

        return super().validate(attrs)
