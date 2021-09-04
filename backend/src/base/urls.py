from django.conf.urls import url, include
from rest_framework import routers
from src.base.views import SettingViewSet
from rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, UserDetailsView,
)

rest_auth_urls = [
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='rest_password_change'),
    url(r'^user/$', UserDetailsView.as_view(), name='user'),
]

router = routers.DefaultRouter()
router.register(r'setting', SettingViewSet, basename='Setting')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include((rest_auth_urls,'auth'),namespace='auth')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
