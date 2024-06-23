from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(post=extend_schema(summary="取得 JWT token (login)"))
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema_view(post=extend_schema(summary="更新 JWT token"))
class CustomTokenRefreshView(TokenRefreshView):
    pass
