"""
URL configuration for fyd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from User.views import UserListAPI, UserDetailAPI, ServerDetailAPI, ServerLikeTagAPI, LikeListAPI, LikeDetailAPI, TagListAPI, TagDetailAPI, MyTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/user/', UserListAPI.as_view()),
    path('api/user/<str:pk>/', UserDetailAPI.as_view()),
    path('api/server/', ServerLikeTagAPI.as_view()),
    path('api/server/<int:pk>/', ServerDetailAPI.as_view()),
    path('api/tag/', TagListAPI.as_view()),
    path('api/tag/<int:server_id>/', TagDetailAPI.as_view()),
    path('api/like/', LikeListAPI.as_view()),
    path('api/like/<int:pk>/', LikeDetailAPI.as_view()),
]

schema_view = get_schema_view( 
    openapi.Info( 
        title="FYI API", 
        default_version="v1", 
        description="Fit Your Discord API Document.\n\
                    Login, Register을 제외한 모든 API는 'Bearer (access token)'이 header에 추가되어야합니다.", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="test", email="test@test.com"), 
        license=openapi.License(name="Test License"), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,), 
)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),    ]
