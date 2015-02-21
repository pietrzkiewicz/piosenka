from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from blog.forms import PostForm
from blog.models import Post
from piosenka.mixins import CheckAuthorshipMixin, CheckLoginMixin
from piosenka.mixins import ContentItemViewMixin


def obsolete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponsePermanentRedirect(post.get_absolute_url())


class PostIndex(TemplateView):
    MAX_POSTS = 5
    template_name = "blog/post_index.html"

    def get_context_data(self, **kwargs):
        context = super(PostIndex, self).get_context_data(**kwargs)
        context['new_posts'] = Post.items_visible_to(self.request.user)\
                                   .all()[0:PostIndex.MAX_POSTS]
        context['all_posts'] = Post.items_visible_to(self.request.user).all()
        return context


class PostDetail(ContentItemViewMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['all_posts'] = Post.items_visible_to(self.request.user).all()
        return context


class AddPost(CheckLoginMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/add_edit_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddPost, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditPost(CheckAuthorshipMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/add_edit_post.html"

    def get_object(self):
        import datetime
        import time
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        slug = self.kwargs['slug']
        date_stamp = time.strptime(year+month+day, "%Y%m%d")
        pub_date = datetime.date(*date_stamp[:3])
        return Post.objects.get(slug=slug,
                                pub_date__year=pub_date.year,
                                pub_date__month=pub_date.month,
                                pub_date__day=pub_date.day)

    def get_success_url(self):
        return self.object.get_absolute_url()
