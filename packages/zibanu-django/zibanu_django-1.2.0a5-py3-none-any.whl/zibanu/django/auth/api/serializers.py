# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/04/23 9:58
# Project:      Django Plugins
# Module Name:  serializers
# Description:
# ****************************************************************
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken
from typing import Dict, Any
from zibanu.django.auth.models import UserProfile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("timezone", "theme", "lang", "avatar", "messages_timeout", "keep_logged_in", "app_profile")

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(default="Guest")
    profile = ProfileSerializer(required=True, read_only=False)
    roles = serializers.SerializerMethodField(default=[])
    user_permissions = serializers.SerializerMethodField(default=[])

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "full_name", "is_staff", "is_superuser", "last_login", "profile", "roles", "user_permissions")

    def get_user_permissions(self, instance) -> list:
        user_permissions = []
        if self.context.get("load_permissions", settings.ZB_AUTH_INCLUDE_PERMISSIONS):
            for user_permission in instance.user_permissions.all():
                user_permissions.append(user_permission.code)
        return user_permissions

    def get_roles(self, instance) -> list:
        roles = []
        if self.context.get("load_roles", settings.ZB_AUTH_INCLUDE_GROUPS):
            for group in instance.user_permissions.all():
                roles.append(group.name)
        return roles

    def get_full_name(self, instance) -> str:
        return instance.get_full_name()





class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = get_user_model().EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Include user data
        user_serializer = UserSerializer(instance=user)
        token["user"] = user_serializer.data

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        user = get_user_model().objects.filter(email__iexact=attrs.get(self.username_field)).first()

        if user is None:
            raise AuthenticationFailed(self.error_messages["no_active_account"], "no_active_account")

        authenticate_kwargs = {
            get_user_model().USERNAME_FIELD: user.get_username(),
            "password": attrs.get("password")
        }
        self.user = authenticate(**authenticate_kwargs)
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        return {}


class TokenObtainSlidingSerializer(EmailTokenObtainSerializer):
    token_class = SlidingToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data["token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
