from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import consumers

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/uploadImage", views.UploadImage, name="UploadImage"),
    path("accounts/register", views.register, name="register"),
    path(
        "accounts/login",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("accounts/logout", auth_views.LogoutView.as_view(), name="logout"),
    path("test", views.test, name="wstests")
    # path("ws/socket-server", consumers.MsgConsumer.as_asgi()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
