from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic as views
# from django.contrib.auth import forms as auth_forms
from django.shortcuts import get_object_or_404
from .forms import CustomRegisterUserForm, CommentForm
from final_exam.easy_drive_ad.models import Ad
from final_exam.easy_drive_profile.models import Profile

# Create your views here.
UserModel = get_user_model()


class ErrorMixin:
    def handle_no_permission(self, message="No permission to modify this resource!"):
        # Custom handling when test_func fails (user does not have permission)
        return render(self.request, '404.html', {'exception_message': message}, status=404)


class Homepage(views.ListView):
    template_name = 'homepage.html'
    model = Ad

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context


"""User Views"""


class LoginUser(auth_views.LoginView):
    template_name = 'user/login.html'
    model = UserModel


class RegisterUser(views.CreateView):
    template_name = 'user/register.html'
    model = UserModel
    form_class = CustomRegisterUserForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a Profile instance for the newly registered user
        Profile.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class LogoutUser(auth_views.LogoutView):
    # template_name = 'user/logout.html'
    pass


class EditUsername(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = UserModel
    template_name = 'user/edit_username.html'
    fields = ['username']

    def get_success_url(self):
        return reverse_lazy('details_profile', kwargs={'pk': self.get_object().profile.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(UserModel, pk=pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this username!")


class DeleteUser(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    """
        Deleting the MyUser instance will delete Profile and Ad instances.
    """
    model = UserModel
    template_name = 'user/delete.html'
    success_url = reverse_lazy('register_user')

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(UserModel, pk=pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to delete this profile!")


class ChangePassword(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, auth_views.PasswordChangeView):
    template_name = 'user/change_password.html'
    model = UserModel

    def get_success_url(self):
        return reverse_lazy('details_profile', kwargs={'pk': self.get_object().profile.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context

    def get_object(self):
        pk = self.kwargs['user_pk']
        return get_object_or_404(UserModel, pk=pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to change this password!")

