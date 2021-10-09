from django.urls import path

from pdoing.users.api.views import obtain_auth_token

app_name = "users"
urlpatterns = [
    path("auth-token/", obtain_auth_token),
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
