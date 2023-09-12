from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from final_exam.easy_drive_ad.models import Ad
from final_exam.easy_drive_blog.models import BlogPost
from final_exam.easy_drive_profile.models import Profile
from final_exam.easy_drive_reactions.models import Like, Comment

from final_exam.easy_drive.forms import CommentForm
from final_exam.easy_drive.views import ErrorMixin

# Create your views here.
UserModel = get_user_model()


"""Like views"""


@login_required(login_url=reverse_lazy('login_user'))
def create_like(request, blog_pk):
    requested_blog = get_object_or_404(BlogPost, pk=blog_pk)
    user_profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    Like.objects.create(owner=user_profile, blog=requested_blog)
    return redirect('details_blog', pk=requested_blog.pk)


@login_required(login_url=reverse_lazy('login_user'))
def remove_like(request, blog_pk):
    like_instance = Like.objects.filter(blog_id=blog_pk, owner_id=request.user.profile.pk).first()

    if request.user.profile.pk != like_instance.owner_id:
        raise Http404("You are not the owner of this like!")

    like_instance.delete()
    return redirect('details_blog', pk=blog_pk)


"""Comment views"""


@login_required(login_url=reverse_lazy('login_user'))
def create_comment(request, ad_pk):
    user_profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    requested_ad = get_object_or_404(Ad, pk=ad_pk)

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
    model = Comment

    def get_success_url(self):
        # return reverse_lazy('homepage' + f'#{self.get_object().ad_id}')
        return reverse_lazy('homepage')

    def get_object(self, queryset=None):
        pk = self.kwargs['comment_pk']
        return get_object_or_404(Comment, pk=pk)

    def test_func(self):
        return self.get_object().owner_id == self.request.user.profile.pk

    def handle_no_permission(self):
        return super().handle_no_permission(message="You do not have permission to edit this comment!")


@login_required(login_url=reverse_lazy('login_user'))
def delete_comment(request, comment_pk):
    requested_comment = get_object_or_404(Comment, pk=comment_pk)
    # current_ad_pk = get_object_or_404(my_models.Ad, pk=requested_comment.ad.pk)
    if request.user.profile.pk != requested_comment.owner_id:
        raise Http404("You are not the author of this comment!")

    requested_comment.delete()
    # return redirect('homepage' + f"#{current_ad_pk}")
    return redirect('homepage')
