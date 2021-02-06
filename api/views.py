from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .mixins import CustomViewSet
from .models import Category, Genre, Review, Title
from .permissions import IsAuthorOrStaff, PermissionMixin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
)


class TitleViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    Выводим все произведения. Используем класс ModelViewSet,
    чтобы получить полный набор операций чтения и записи по умолчанию.
    Делаем фильтр по нужным полям.
    """

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TitleCreateSerializer
        return TitleReadSerializer


class CategoryViewSet(PermissionMixin, CustomViewSet):
    """
    Выводим все категории. Используем класс CustomViewSet,
    для предоставления действий, которые используются для обеспечения
    основного поведения представлений. Делаем search по нужному полю.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(PermissionMixin, CustomViewSet):
    """
    Выводим все жанры. Используем класс CustomViewSet,
    для предоставления действий, которые используются для обеспечения
    основного поведения представлений. Делаем search по нужному полю.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получить список всех отзывов. Доступ: без токена. Создать новый отзыв.
    Доступ: аутентифицированные пользователи. Получить отзыв по id. Доступ:
    без токена. Частично обновить отзыв по id. Доступ: автор отзыва,
    модератор или администратор. Удалить отзыв по id. Доступ: автор отзыва,
    модератор или администратор.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrStaff,
    )

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)

        return title

    def get_queryset(self):
        title = self.get_title()

        return title.reviews.all()

    def rating_update(self, serializer):
        title = self.get_title()

        serializer.save(author=self.request.user, title_id=title.id)

        title.rating = Review.objects.filter(title=title).aggregate(
            Avg("score")
        )["score__avg"]
        title.save(update_fields=["rating"])

    def perform_create(self, serializer):
        self.rating_update(serializer)

    def perform_update(self, serializer):
        self.rating_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получить список всех комментариев к отзыву по id. Доступ: без токена.
    Создать новый комментарий для отзыва. Доступ: аутентифицированные
    пользователи. Получить комментарий для отзыва по id. Доступ: без токена.
    Частично обновить комментарий к отзыву по id. Доступ: автор отзыва,
    модератор или администратор. Удалить комментрий к отзыву по id. Доступ:
    автор отзыва, модератор или администратор.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrStaff,
    )

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, id=review_id, title__id=title_id)

        return review

    def get_queryset(self):
        review = self.get_review()

        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()

        serializer.save(author=self.request.user, review_id=review.id)
