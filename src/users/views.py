import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # type: ignore
from drf_spectacular.utils import extend_schema  # type: ignore
from rest_framework import  permissions # type: ignore
logger = logging.getLogger(__name__)


def set_auth_cookies(
    response: Response, access_token: str, refresh_token: Optional[str] = None
) -> None:
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime,
    }
    response.set_cookie("access", access_token, **cookie_settings)

    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT[
            "REFRESH_TOKEN_LIFETIME"
        ].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)

@extend_schema(tags=["Auth"])
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        token_res = super().post(request, *args, **kwargs)

        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    token_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)

                token_res.data["message"] = "Login Successful."
            else:
                token_res.data["message"] = "Login Failed"
                logger.error("Access or refresh token not found in login response data")

        return token_res

@extend_schema(tags=["Auth"])
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        refresh_res = super().post(request, *args, **kwargs)

        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get("access")
            refresh_token = refresh_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    refresh_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                refresh_res.data["message"] = "Access tokens refreshed successfully"
            else:
                refresh_res.data["message"] = (
                    "Access or refresh tokens not found in refresh response data"
                )
                logger.error(
                    "Access or refresh token not found in refresh response data"
                )

        return refresh_res

@extend_schema(tags=["Auth"])
class CustomProviderAuthView(ProviderAuthView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        provider_res = super().post(request, *args, **kwargs)

        if provider_res.status_code == status.HTTP_201_CREATED:
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    provider_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)

                provider_res.data["message"] = "You are logged in Successful."
            else:
                provider_res.data["message"] = (
                    "Access or refresh token not found in provider response"
                )
                logger.error(
                    "Access or refresh token not found in provider response data"
                )

        return provider_res

@extend_schema(tags=["Auth"])
class LogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):
        from django.core import mail
        emails = (
            ('Hey Man', "I'm The Dude! So that's what you call me.", 'dude@aol.com', ['mr@lebowski.com']),
            ('Dammit Walter', "Let's go bowlin'.", 'dude@aol.com', ['wsobchak@vfw.org']),
        )
        results = mail.send_mass_mail(emails)
        print(results)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        # response.delete_cookie("access")
        # response.delete_cookie("refresh")
        # response.delete_cookie("logged_in")
        return response
