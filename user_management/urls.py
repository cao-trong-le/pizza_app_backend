from django.urls import path
from .views import NewUserView, BlacklistTokenUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', NewUserView.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]