from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router_v1_auth = [
    path("email/", views.get_confirmation_code),
    path("token/", views.get_jwt_token),
    path("refresh/", views.refresh_confirmation_code),
]

router_v1 = DefaultRouter()

router_v1.register("users", views.UserViewSet, basename="users")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/auth/", include(router_v1_auth)),
    path("v1/", include(router_v1.urls)),
]
