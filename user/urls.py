from django.urls import path
from user import views as user_views


urlpatterns = [

    path('', user_views.user_profile_detail_view.as_view(),
         name="user_profile_detail"),

    path('profile/<int:pk>/',
         user_views.profile_detail_view.as_view(), name="profile_detail"),

    path('profile/update/', user_views.update_profile.as_view(),
         name="profile_update")
         
]
