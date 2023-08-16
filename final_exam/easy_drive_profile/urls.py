from django.urls import path
from final_exam.easy_drive_profile import views

urlpatterns = [
    path('details/<int:pk>/', views.ProfileDetails.as_view(), name='details_profile'),
    path('edit/<int:pk>/', views.EditProfile.as_view(), name="edit_profile"),
]
