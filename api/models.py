from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import datetime

from users.models import User


class Genre(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        db_table = "genre"
        verbose_name = "genre"
        verbose_name_plural = "genres"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(
        "Год выпуска",
        validators=[
            MaxValueValidator(datetime.datetime.now().year),
        ],
    )
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        db_column="category",
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", blank=True, db_table="genre_title"
    )

    class Meta:
        db_table = "titles"
        verbose_name = "title"
        verbose_name_plural = "titles"
        ordering = ["name"]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        related_name="reviews",
        db_column="title_id",
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор отзыва",
        related_name="reviews",
        db_column="author",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка произведения",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10, message="Максимально возможная оценка - 10"),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации отзыва",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = "review"
        ordering = ["-pub_date"]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        related_name="comments",
        db_column="review_id",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
        db_column="author",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации комментария", auto_now_add=True
    )

    class Meta:
        db_table = "comments"
        ordering = ["-pub_date"]
