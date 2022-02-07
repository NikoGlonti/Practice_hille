from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from .forms import RegisterForm, ContactUsForm
from .models import Comment, Post, User


def index(request):
    num_posts = Post.objects.count()
    num_comments = Comment.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_posts': num_posts, 'num_comments': num_comments,
                 'num_visits': num_visits},
    )


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = 'update_user.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PostListView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'post_list.html'


@method_decorator(cache_page(30), name='dispatch')
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


class CreatePost(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    success_message = 'Author successfully created'
    template_name = "create_post.html"
    fields = ('title', 'brief_description', 'full_description', 'image', 'posted')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        send_mail(
            'Post',
            'Create new post',
            'nik@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )

        return super(CreatePost, self).form_valid(form)


# def create_post(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = PostCreate(request.POST)
#             if form.is_valid():
#                 title = form.cleaned_data['title']
#                 brief_description = form.cleaned_data['brief_description']
#                 full_description = form.cleaned_data['full_description']
#                 posted = form.cleaned_data['posted']
#                 author = request.user
#                 post = Post.objects.create(title=title, brief_description=brief_description,
#                                            full_description=full_description,
#                                            posted=posted, author=author)
#                 post.save()
#         else:
#             form = PostCreate()
#         return render(request, 'create_post.html', {'form': form})
#     return HttpResponseRedirect('')


class MyCommentView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = 'my_comments.html'
    paginate_by = 10

    def get_queryset(self):
        return Comment.objects.filter(username=self.request.user).filter(posted_com=True)


# def comment_create(request,):
#     if request.method == 'POST':
#         form = CommentCreate(request.POST)
#         username = request.user
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             Comment.objects.create(username=username, text=text)
#             return HttpResponseRedirect(reverse_lazy(''))
#     else:
#         form = CommentCreate()
#     return render(request, 'create_comment.html', {'form': form, })

class CommentCreateView(SuccessMessageMixin, generic.CreateView):
    template_name = 'create_comment.html'
    model = Comment
    fields = ('username', "text", 'post')
    success_message = 'Comment successfully created'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def get_initial(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return {
            'post': post
        }

    def form_valid(self, form):
        send_mail(
            'Comment',
            'Create new comment',
            'nik@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )
        return super(CommentCreateView, self).form_valid(form)


@method_decorator(cache_page(30), name='dispatch')
class ProfileInfo(generic.DetailView):
    model = User
    template_name = "profile_info.html"


@method_decorator(cache_page(30), name='dispatch')
class ProfileList(generic.ListView):
    queryset = User.objects.all()
    template_name = "profile_list.html"


class MessageAdmin(SuccessMessageMixin, generic.FormView):
    form_class = ContactUsForm
    success_message = 'Message send'
    success_url = reverse_lazy('index')
    template_name = 'contact_us.html'

    def form_valid(self, form):
        data = form.cleaned_data
        send_mail('MESSAGE',
                  data['text'],
                  'admin@gmail.com',
                  ['problem@gmail.com'],
                  fail_silently=False,
                  )
        return super(MessageAdmin, self).form_valid(form)
