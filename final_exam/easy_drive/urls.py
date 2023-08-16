from django.urls import path
from final_exam.easy_drive import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('login/', views.LoginUser.as_view(), name='login_user'),
    path('logout/', views.LogoutUser.as_view(), name='logout_user'),
    path('edit/username/<int:pk>/', views.EditUsername.as_view(), name="edit_username"),
    path('change-password/<int:pk>/', views.ChangePassword.as_view(), name="change_password"),
    path('delete-user/<int:pk>/', views.DeleteUser.as_view(), name="delete_user"),
]
