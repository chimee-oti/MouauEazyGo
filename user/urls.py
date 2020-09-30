from django.urls import path
from user import views as user_views


urlpatterns = [

    path('', user_views.user_profile_detail.as_view(),
         name="user_profile_detail"),

    path('profile/<int:pk>/',
         user_views.profile_detail_view.as_view(), name="profile_detail"),

    path('profile/update/<int:pk>/',
         user_views.profile_update_view.as_view(), name="profile_update"),

    path('login/', user_views.login_view.as_view(), name="login"),

    path('logout/', user_views.logout_view.as_view(), name="logout"),

    path('register/', user_views.user_register_view.as_view(), name="register"),

    path('password-change', user_views.password_change_view.as_view(),
         name="password_change"),

    path('password-change-done', user_views.password_change_done_view.as_view(),
         name="password_change_done"),

    path('password-reset/', user_views.password_reset_view.as_view(),
         name="password_reset"),

    path('password-reset-done/', user_views.password_reset_done_view.as_view(),
         name="password_reset_done.html"),

    path('password-reset-confirm/<uidb64>/<token>/',
         user_views.password_reset_confirm_view.as_view(), name="password_reset_confirm"),

    path('password-reset-complete/', user_views.password_reset_complete_view.as_view(),
         name="password_reset_complete"),
]
