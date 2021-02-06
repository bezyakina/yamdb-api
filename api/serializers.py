from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        exclude = ("title",)

    def validate(self, attrs):

        if (
            Review.objects.filter(
                author=self.context["request"].user, title=self.get_title()
            ).exists()
            and self.context["request"].method != "PATCH"
        ):
            raise serializers.ValidationError("Вы уже оставили отзыв")

        return attrs

    def get_title(self):
        title = get_object_or_404(
            Title, id=self.context.get("view").kwargs.get("title_id")
        )

        return title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        exclude = ("review",)
