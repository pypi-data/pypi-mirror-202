# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         11/02/23 12:25
# Project:      CFHL Transactional Backend
# Module Name:  viewset
# Description:
# ****************************************************************
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.viewsets import ViewSet as RestViewSet
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.models import TokenUser


class ViewSet(RestViewSet):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    if settings.DEBUG:
        authentication_classes.append(authentication.TokenAuthentication)

    def _get_user(self, request):
        # If user is from simplejwt
        user = request.user
        if isinstance(request.user, TokenUser):
            user = get_user_model().objects.get(pk=request.user.id)
        return user
