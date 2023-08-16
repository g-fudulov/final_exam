from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from final_exam.easy_drive_blog.models import BlogPost
from final_exam.easy_drive_profile.models import Profile
from final_exam.easy_drive_reactions.models import Like

from final_exam.easy_drive.views import ErrorMixin

# Create your views here.

UserModel = get_user_model()


class ShowBlogs(views.ListView):
    template_name = 'blog/show_blogs.html'
    model = BlogPost


class CreateBlog(LoginRequiredMixin, views.CreateView):
    template_name = "blog/create.html"
    model = BlogPost
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
    model = BlogPost

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(BlogPost, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_profile'] = Profile.objects.filter(pk=self.get_object().owner_id).first()
        # context['author_user'] = UserModel.objects.filter(pk=self.get_object().owner_id).first()
        context['author_user'] = UserModel.objects.filter(pk=context['author_profile'].user_id).first()
        context['all_likes'] = Like.objects.filter(blog_id=self.get_object().pk).count()
        if self.request.user.is_authenticated:
            context['like_instance'] = Like.objects.filter(blog_id=self.get_object().pk,
                                                           owner_id=self.request.user.profile.pk).first()
        return context


class DeleteBlog(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    template_name = 'blog/delete.html'
    model = BlogPost
    success_url = reverse_lazy('show_blogs')

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(BlogPost, pk=pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.user_id

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to delete this Blog!")


class EditBlog(ErrorMixin, LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    template_name = 'blog/edit.html'
    model = BlogPost
    fields = ['title', 'topic', 'content']

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(BlogPost, pk=pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.user_id

    def get_success_url(self):
        return reverse_lazy('details_blog', kwargs={"pk": self.get_object().pk})

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this Blog!")
