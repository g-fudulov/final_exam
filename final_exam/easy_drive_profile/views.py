from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from final_exam.easy_drive_profile.models import Profile
from final_exam.easy_drive_blog.models import BlogPost
from final_exam.easy_drive_ad.models import Ad

from final_exam.easy_drive.views import ErrorMixin

# Create your views here.

UserModel = get_user_model()

"""Profile Views"""


class EditProfile(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    template_name = "user/edit.html"
    model = Profile
    fields = ['first_name', 'last_name', 'phone_number']

    def get_success_url(self):
        return reverse_lazy('details_profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(Profile, pk=pk)

    def test_func(self):
        requested_profile = self.get_object()
        return requested_profile.user_id == self.request.user.pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this profile.")


class ProfileDetails(views.DetailView):
    template_name = 'user/details.html'
    model = Profile

    def get_object(self, queryset=None, **kwargs):
        pk = self.kwargs['pk']
        return get_object_or_404(Profile, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ad_owner_user"] = self.get_owner()
        context['all_ads'] = Ad.objects.filter(owner_id=self.get_object().pk).all()
        context['all_blogs'] = BlogPost.objects.filter(owner_id=self.get_object().pk).all()
        return context

    def get_owner(self):
        # return UserModel.objects.filter(pk=self.kwargs['pk']).first()
        # return UserModel.objects.filter(pk=self.get_object().user_id).first()
        return get_object_or_404(UserModel, pk=self.get_object().user_id)