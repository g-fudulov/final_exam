from django.urls import path
from final_exam.easy_drive_ad import views

urlpatterns = [
    path('create/', views.CreateAd.as_view(), name='create_ad'),
    path('delete/<int:pk>', views.DeleteAd.as_view(), name='delete_ad'),
    path('edit/<int:pk>/', views.EditAd.as_view(), name='edit_ad'),
    path('details/<int:pk>/', views.DetailsAd.as_view(), name='details_ad'),
]
