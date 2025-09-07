from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, \
    SpectacularAPIView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from api.v1.views import AuthorViewSet, BookViewSet


router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
    path("token/", TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
]
