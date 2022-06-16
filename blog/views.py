from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Comment
from django.contrib import messages
from .forms import CommentForm, PostForm, ContactForm
from django.contrib.auth.decorators import login_required


def handler_403(request, exception):
    '''403 error view'''
    return render(request, '403.html', status=403)


def handler_404(request, exception):
    '''
    A 404 error handling view
    '''
    return render(request, '404.html', status=404)


def handler_500(request, *args, **argv):
    '''
    A 500 error handling view
    '''
    return render(request, '500.html', status=500)


# Homepage details
def Homepage(request):
    template_name= 'index.html'
    return render(request, template_name)


#Contact form details
def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True
 
    return render(request, 
        'contact.html', 
        {'form': form, 'submitted': submitted}
        )



class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog.html"
    paginate_by = 6


# Add blog
@login_required
def create_post(request):
    """
    Allow an admin user to create a Blop Post
    """
    if request.user.is_superuser:

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                blog_post = form.save(commit=False)
                blog_post.user = request.user
                blog_post.save()
                messages.info(request, 'Blog added successfully!')
                return redirect(reverse('blog_detail', args=[blog_post.id]))
            else:
                messages.error(request, 'Please check the form for errors. \
                    Blog failed to add.')
        else:
            form = PostForm()
    else:
        messages.error(request, 'Sorry, you do not have permission to do that.')
        return redirect(reverse('home'))

    template = 'add_blog.html'

    context = {
        'form': form,
    }

    return render(request, template, context)

class PostDetail(View):
    """ Post Detail"""

    def get(self, request, blog_post_id):
        post = get_object_or_404(Post, pk=blog_post_id)
        comments = post.comments.filter(post=post).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = {
            "blog_post": post,
            "comments": comments,
            "commented": False,
            "liked": liked,
            "comment_form": CommentForm()
        }
        return render(request, "blog_detail.html", context)

    def post(self, request, blog_post_id):
        """ Post Method"""
        post = get_object_or_404(Post, pk=blog_post_id)
        comments = post.comments.filter(post=post).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        context = {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
                    }
        return redirect(reverse('blog_detail', args=[blog_post_id]))


# Edit Blog Post
@login_required
def edit_blog(request, blog_post_id):
    """
    Allow all users to edit the blogs they created
    """
    if request.user.is_superuser:

        blog_post = get_object_or_404(Post, pk=blog_post_id)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=blog_post)
            if form.is_valid():
                form.save()
                messages.info(request, 'Blog post updated successfully!')
                return redirect(reverse('blog_detail', args=[blog_post.id]))
            else:
                messages.error(request, 'Please check the form for errors. \
                    Blog post failed to update.')
        else:
            form = PostForm(instance=blog_post)
            messages.info(request, f'Editing {blog_post.title}')
    else:
        messages.error(request, 'Sorry, you do not have permission for that.')
        return redirect(reverse('home'))

    template = 'edit_blog.html'

    context = {
        'form': form,
        'blog_post': blog_post,
    }

    return render(request, template, context)


class PostLike(View):
    
    def post(self, request, blog_post_id):
        post = get_object_or_404(Post, blog_post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('blog_detail', 'blog_post_id'))
