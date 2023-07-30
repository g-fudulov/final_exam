from django.urls import path, include
from ..easy_drive import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),

    #  auth views
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('login/', views.LoginUser.as_view(), name='login_user'),
    path('logout/', views.LogoutUser.as_view(), name='logout_user'),

    #  ad views
    path('advertisement/', include([
        path('create/', views.CreateAd.as_view(), name='create_ad'),
        path('delete/<int:pk>', views.DeleteAd.as_view(), name='delete_ad'),
        path('edit/<int:pk>/', views.EditAd.as_view(), name='edit_ad'),
        path('details/<int:pk>/', views.DetailsAd.as_view(), name='details_ad'),

        # comment views
        path('comment/', include([
            path('post/<int:ad_pk>/', views.create_comment, name='create_comment'),
            path('edit/<int:comment_pk>/', views.EditComment.as_view(), name='edit_comment'),
            path('delete/<int:comment_pk>/', views.delete_comment, name='delete_comment')
        ])),
    ])),

    #  profile views
    path('profile/', include([
        path('details/<int:pk>/', views.ProfileDetails.as_view(), name='details_profile'),
        path('edit/<int:pk>/', views.EditProfile.as_view(), name="edit_profile"),
        path("username/edit/<int:pk>/", views.EditUsername.as_view(), name='edit_username'),
        path("delete/<int:pk>/", views.DeleteUser.as_view(), name="delete_user")
    ])),

    # blog views
    path('blog/', include([
        path('home/', views.ShowBlogs.as_view(), name='show_blogs'),
        path('create/', views.CreateBlog.as_view(), name='create_blog'),
        path('details/<int:pk>/', views.DetailsBlog.as_view(), name="details_blog"),
        path('delete/<int:pk>/', views.DeleteBlog.as_view(), name='delete_blog'),
        path('edit/<int:pk>/', views.EditBlog.as_view(), name='edit_blog'),

        # like views
        path('like/<int:blog_pk>/', views.create_like, name='like_create'),
        path('like-remove/<int:blog_pk>', views.remove_like, name='like_remove')
    ])),

]
