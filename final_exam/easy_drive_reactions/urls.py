from django.urls import path, include
from final_exam.easy_drive_reactions import views

urlpatterns = [
    path('like/<int:blog_pk>/', views.create_like, name='like_create'),
    path('like-remove/<int:blog_pk>', views.remove_like, name='like_remove'),
    path('comment/', include([
        path('post/<int:ad_pk>/', views.create_comment, name='create_comment'),
        path('edit/<int:comment_pk>/', views.EditComment.as_view(), name='edit_comment'),
        path('delete/<int:comment_pk>/', views.delete_comment, name='delete_comment')
    ])),
]
