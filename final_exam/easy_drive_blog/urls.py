from django.urls import path
from final_exam.easy_drive_blog import views

urlpatterns = [
    path('home/', views.ShowBlogs.as_view(), name='show_blogs'),
    path('create/', views.CreateBlog.as_view(), name='create_blog'),
    path('details/<int:pk>/', views.DetailsBlog.as_view(), name="details_blog"),
    path('delete/<int:pk>/', views.DeleteBlog.as_view(), name='delete_blog'),
    path('edit/<int:pk>/', views.EditBlog.as_view(), name='edit_blog'),
]
