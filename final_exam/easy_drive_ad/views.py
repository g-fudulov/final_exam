from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from final_exam.easy_drive_profile.models import Profile
from final_exam.easy_drive.forms import CommentForm

from final_exam.easy_drive.views import ErrorMixin
from final_exam.easy_drive_ad.models import Ad

# Create your views here.

UserModel = get_user_model()

class CreateAd(LoginRequiredMixin, views.CreateView):
    model = Ad
    template_name = 'ad/create.html'
    fields = ["cover_photo", "additional_photo", "title", 'price', "description"]

    # success_url = reverse_lazy('homepage')

    def get_success_url(self):
        return reverse_lazy('details_ad', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Get the currently logged-in user's profile
        profile = self.request.user.profile

        # Set the profile as the owner of the newly created Ad
        form.instance.owner = profile
        return super().form_valid(form)


class DeleteAd(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = Ad
    template_name = 'ad/delete.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        requested_ad = self.get_object()
        return requested_ad.owner_id == self.request.user.profile.pk

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return Ad.objects.filter(pk=pk).first()

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to delete this advertisement!")


class EditAd(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = Ad
    template_name = 'ad/edit.html'
    fields = ['title', 'cover_photo', "additional_photo", "price", 'description']

    def get_success_url(self):
        return reverse_lazy('details_ad', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(Ad, pk=pk)

    def test_func(self):
        requested_ad = self.get_object()
        return requested_ad.owner_id == self.request.user.profile.pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this advertisement!")


class DetailsAd(views.DetailView):
    template_name = 'ad/details.html'
    model = Ad

    def get_object(self, *args, **kwargs):
        pk = self.kwargs['pk']
        return get_object_or_404(Ad, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_ad = self.get_object()
        context['author_profile'] = Profile.objects.filter(pk=requested_ad.owner_id).first()
        context['author_user'] = UserModel.objects.filter(pk=requested_ad.owner.user_id).first()
        context['comment_form'] = CommentForm
        return context
