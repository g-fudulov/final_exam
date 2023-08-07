from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic as views
from ..easy_drive import models as my_models
# from django.contrib.auth import forms as auth_forms
from django.shortcuts import get_object_or_404
from .forms import CustomRegisterUserForm, CommentForm

# Create your views here.
UserModel = get_user_model()


class ErrorMixin:
    def handle_no_permission(self, message="No permission to modify this resource!"):
        # Custom handling when test_func fails (user does not have permission)
        return render(self.request, '404.html', {'exception_message': message}, status=404)


class Homepage(views.ListView):
    template_name = 'homepage.html'
    model = my_models.Ad

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
        my_models.Profile.objects.create(user=self.object)
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
        return reverse_lazy('details_profile', kwargs={'pk': self.get_object().pk})

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


"""Profile Views"""


class EditProfile(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    template_name = "user/edit.html"
    model = my_models.Profile
    fields = ['first_name', 'last_name', 'phone_number']

    def get_success_url(self):
        return reverse_lazy('details_profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(my_models.Profile, pk=pk)

    def test_func(self):
        requested_profile = self.get_object()
        return requested_profile.user_id == self.request.user.pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this profile.")


class ProfileDetails(views.DetailView):
    template_name = 'user/details.html'
    model = my_models.Profile

    def get_object(self, queryset=None, **kwargs):
        pk = self.kwargs['pk']
        return get_object_or_404(my_models.Profile, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ad_owner_user"] = self.get_owner()
        context['all_ads'] = my_models.Ad.objects.filter(owner_id=self.get_object().pk).all()
        context['all_blogs'] = my_models.BlogPost.objects.filter(owner_id=self.get_object().pk).all()
        return context

    def get_owner(self):
        # return UserModel.objects.filter(pk=self.kwargs['pk']).first()
        # return UserModel.objects.filter(pk=self.get_object().user_id).first()
        return get_object_or_404(UserModel, pk=self.get_object().user_id)


"""Ad Views"""


class CreateAd(LoginRequiredMixin, views.CreateView):
    model = my_models.Ad
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
    model = my_models.Ad
    template_name = 'ad/delete.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        requested_ad = self.get_object()
        return requested_ad.owner_id == self.request.user.profile.pk

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return my_models.Ad.objects.filter(pk=pk).first()

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to delete this advertisement!")


class EditAd(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = my_models.Ad
    template_name = 'ad/edit.html'
    fields = ['title', 'cover_photo', "additional_photo", "price", 'description']

    def get_success_url(self):
        return reverse_lazy('details_ad', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(my_models.Ad, pk=pk)

    def test_func(self):
        requested_ad = self.get_object()
        return requested_ad.owner_id == self.request.user.profile.pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this advertisement!")


class DetailsAd(views.DetailView):
    template_name = 'ad/details.html'
    model = my_models.Ad

    def get_object(self, *args, **kwargs):
        pk = self.kwargs['pk']
        return get_object_or_404(my_models.Ad, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_ad = self.get_object()
        context['author_profile'] = my_models.Profile.objects.filter(pk=requested_ad.owner_id).first()
        context['author_user'] = UserModel.objects.filter(pk=requested_ad.owner.user_id).first()
        context['comment_form'] = CommentForm
        return context


"""Blog Views"""


class ShowBlogs(views.ListView):
    template_name = 'blog/show_blogs.html'
    model = my_models.BlogPost


class CreateBlog(LoginRequiredMixin, views.CreateView):
    template_name = "blog/create.html"
    model = my_models.BlogPost
    fields = ['title', 'topic', 'content']

    def get_success_url(self):
        return reverse_lazy('details_blog', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Get the currently logged-in user's profile
        profile = self.request.user.profile

        # Set the profile as the owner of the newly created Blog post
        form.instance.owner = profile
        return super().form_valid(form)


class DetailsBlog(views.DetailView):
    template_name = 'blog/details.html'
    model = my_models.BlogPost

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(my_models.BlogPost, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_profile'] = my_models.Profile.objects.filter(pk=self.get_object().owner_id).first()
        # context['author_user'] = UserModel.objects.filter(pk=self.get_object().owner_id).first()
        context['author_user'] = UserModel.objects.filter(pk=context['author_profile'].user_id).first()
        context['all_likes'] = my_models.Like.objects.filter(blog_id=self.get_object().pk).count()
        if self.request.user.is_authenticated:
            context['like_instance'] = my_models.Like.objects.filter(blog_id=self.get_object().pk, owner_id=self.request.user.profile.pk).first()
        return context


class DeleteBlog(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    template_name = 'blog/delete.html'
    model = my_models.BlogPost
    success_url = reverse_lazy('show_blogs')

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(my_models.BlogPost, pk=pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.user_id

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to delete this Blog!")


class EditBlog(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    template_name = 'blog/edit.html'
    model = my_models.BlogPost
    fields = ['title', 'topic', 'content']

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(my_models.BlogPost, pk=pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.user_id

    def get_success_url(self):
        return reverse_lazy('details_blog', kwargs={"pk": self.get_object().pk})

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this Blog!")


"""Like views"""


@login_required(login_url=reverse_lazy('login_user'))
def create_like(request, blog_pk):
    requested_blog = get_object_or_404(my_models.BlogPost, pk=blog_pk)
    user_profile = get_object_or_404(my_models.Profile, pk=request.user.profile.pk)
    my_models.Like.objects.create(owner=user_profile, blog=requested_blog)
    return redirect('details_blog', pk=requested_blog.pk)


@login_required(login_url=reverse_lazy('login_user'))
def remove_like(request, blog_pk):
    like_instance = my_models.Like.objects.filter(blog_id=blog_pk, owner_id=request.user.profile.pk).first()

    if request.user.profile.pk != like_instance.owner_id:
        raise Http404("You are not the author of this comment!")

    like_instance.delete()
    return redirect('details_blog', pk=blog_pk)


"""Comment views"""


@login_required(login_url=reverse_lazy('login_user'))
def create_comment(request, ad_pk):
    user_profile = get_object_or_404(my_models.Profile, pk=request.user.profile.pk)
    requested_ad = get_object_or_404(my_models.Ad, pk=ad_pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.owner = user_profile
            form.instance.ad = requested_ad
            form.save()
            # my_models.Comment.objects.create(owner=user_profile, ad=requested_ad)

    context = {
        'comment_form': form
    }
    return redirect(request.META['HTTP_REFERER'] + f"#{ad_pk}", context=context)


class EditComment(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    template_name = 'comment/edit.html'
    fields = ['content', ]
    model = my_models.Comment

    def get_success_url(self):
        # return reverse_lazy('homepage' + f'#{self.get_object().ad_id}')
        return reverse_lazy('homepage')

    def get_object(self, queryset=None):
        pk = self.kwargs['comment_pk']
        return get_object_or_404(my_models.Comment, pk=pk)

    def test_func(self):
        return self.get_object().owner_id == self.request.user.profile.pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this comment!")


@login_required(login_url=reverse_lazy('login_user'))
def delete_comment(request, comment_pk):
    requested_comment = get_object_or_404(my_models.Comment, pk=comment_pk)
    # current_ad_pk = get_object_or_404(my_models.Ad, pk=requested_comment.ad.pk)
    if request.user.profile.pk != requested_comment.owner_id:
        raise Http404("You are not the author of this comment!")

    requested_comment.delete()
    # return redirect('homepage' + f"#{current_ad_pk}")
    return redirect('homepage')
