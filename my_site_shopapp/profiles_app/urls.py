from django.urls import path

from .views import ProfilesDetailView, ProfilesListView, ProfilesUpdateView

app_name = "profiles"

urlpatterns = [
    path("user/<str:username>/", ProfilesDetailView.as_view(), name="profiles_detail"),
    path(
        "user/<str:username>/edit", ProfilesUpdateView.as_view(), name="profiles_edit"
    ),
    path("list/", ProfilesListView.as_view(), name="profiles_list"),
]
