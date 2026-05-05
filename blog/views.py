from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from odf import form

from .forms import *
from django.db.models import Max
from django.db.models.functions import Coalesce, Greatest

def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)

@superuser_required(login_url='login')
def CreatePost(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post-list')
    context = {
        'form': form,
    }
    return render(request, 'post/create-post.html', context)

@superuser_required(login_url='login')
def UpdatePost(request, id):
    post = blogPosts.objects.get(id=id)
    forms = CreatePostForm(instance=post)
    if request.method == 'POST':
        forms = CreatePostForm(request.POST, request.FILES, instance=post)
        if forms.is_valid():
            forms.save()
            return redirect('post-list')
    context = {
        'form': forms,
        'post': post
    }
    return render(request, 'post/create-post.html', context)

@superuser_required(login_url='login')
def DeletePost(request, id):
    post = blogPosts.objects.get(id=id)
    post.delete()
    return redirect('post-list')

@superuser_required(login_url='login')
def ListPost(request):
    cats = PostCategory.objects.all()
    context = {
        'cats': cats
    }
    return render(request, 'post/list-post.html', context)


## Blog Category CRUD Functions
@superuser_required(login_url='login')
def CreatePostCategory(request):
    forms = CreatePostCategoryForm()
    if request.method == 'POST':
        forms = CreatePostCategoryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('post-category-list')
    context = {
        'form': forms
    }
    return render(request, 'post/create-post-category.html', context)

@superuser_required(login_url='login')
def UpdatePostCategory(request, id):
    category = PostCategory.objects.get(id=id)
    forms = CreatePostCategoryForm(instance=category)
    if request.method == 'POST':
        forms = CreatePostCategoryForm(request.POST, instance=category)
        if forms.is_valid():
            forms.save()
            return redirect('post-category-list')
    context = {
        'form': forms
    }
    return render(request, 'post/create-post-category.html', context)

@superuser_required(login_url='login')
def DeletPostCategory(request, id):
    category = PostCategory.objects.get(id=id)
    category.delete()
    return redirect('post-category-list')

@superuser_required(login_url='login')
def PostCategoryList(request):
    return render(request, 'post/category-list.html')

@superuser_required(login_url='login')
def comments_list(request):
    all_comments_qs = comments.objects.annotate(
    last_reply_date=Max('reply_comments__create_date'),
       ).annotate(
    last_activity=Greatest('create_date', Coalesce('last_reply_date', 'create_date'))
       ).order_by('-last_activity', '-id')
    paginator = Paginator(all_comments_qs, 10)
    pagenumber = request.GET.get('page')
    all_comments = paginator.get_page(pagenumber)

    # فقط reply های مربوط به کامنت‌های همین صفحه
    comment_ids = [c.id for c in all_comments]
    replies = reply_comments.objects.filter(comment_id__in=comment_ids).order_by('-id')

    # گروه‌بندی reply ها برای هر کامنت
    replies_by_comment = {}
    for r in replies:
        replies_by_comment.setdefault(r.comment_id, []).append(r)

    # بچسباندن reply ها به هر کامنت (تا تو template راحت باشه)
    for c in all_comments:
        c.replies = replies_by_comment.get(c.id, [])

    context = {
        'all_comments': all_comments
    }
    return render(request, 'post/comments.html', context)

@superuser_required(login_url='login')
def update_comment(request, id):
    comment = comments.objects.get(id=id)
    all_reply = reply_comments.objects.filter(comment=comment)
    if 'publish' in request.POST:
        publish = request.POST.get('publish')
        if publish == '1':
            comment.publish = True
            comment.save()
            return redirect('comments_list')
        if publish == '0':
            comment.publish = False
            comment.save()
            return redirect('comments_list')
    context = {
        'comment': comment,
        'all_reply': all_reply
    }
    return render(request, 'post/update_comment.html', context)


@superuser_required(login_url='login')
def delete_comment(request, id):
    comment = comments.objects.get(id=id)
    comment.delete()
    return redirect('comments_list')

@superuser_required(login_url='login')
def ajax_related_pst(request):
    category = request.GET.get('category')
    all_posts = blogPosts.objects.filter(Category=category)
    context = {
        'all_posts': all_posts
    }
    return render(request, 'blog/ajax_post_list.html', context)

@superuser_required(login_url='login')
def add_related_post(request, id):
    post = blogPosts.objects.get(id=id)
    categories = PostCategory.objects.all()
    all_related = related_posts.objects.filter(post=post)
    forms = relatedPostForm()
    if request.method == 'POST':
        forms = relatedPostForm(request.POST)
        if forms.is_valid():
            new = forms.save(commit=False)
            new.post = post
            new.save()
            return redirect('add_related_post', post.id)
        else:
            return redirect('add_related_post', post.id)
    context = {
        'form': forms,
        'post': post,
        'categories': categories,
        'all_related': all_related
    }
    return render(request, 'blog/related_post.html', context)

@superuser_required(login_url='login')
def update_related_post(request, id):
    categories = PostCategory.objects.all()
    related_item = related_posts.objects.get(id=id)
    all_related = related_posts.objects.filter(post=related_item.post)
    forms = relatedPostForm(instance=related_item)
    if request.method == 'POST':
        forms = relatedPostForm(request.POST, instance=related_item)
        if forms.is_valid():
            new = forms.save(commit=False)
            new.save()
            return redirect('add_related_post', related_item.post.id)
    context = {
        'form': forms,
        'post': related_item.post,
        'categories': categories,
        'all_related': all_related,
        'related_item': related_item
    }
    return render(request, 'blog/related_post.html', context)

@superuser_required(login_url='login')
def delete_related_post(request, id):
    related_item = related_posts.objects.get(id=id)
    post_id = related_item.post.id
    related_item.delete()
    return redirect('add_related_post', post_id)

@superuser_required(login_url='login')
def publish_reply(request, id):
    reply = reply_comments.objects.get(id=id)
    reply.publish = True
    reply.save()
    return redirect('update_comment', reply.comment.id)

@superuser_required(login_url='login')
def remove_reply(request, id):
    reply = reply_comments.objects.get(id=id)
    comment = reply.comment
    reply.delete()
    return redirect(request.META.get('HTTP_REFERER', 'comments_list'))

@superuser_required(login_url='login')
def toggle_reply_publish(request, id):
    reply = reply_comments.objects.get(id=id)
    reply.publish = not reply.publish
    reply.save()
    return redirect(request.META.get('HTTP_REFERER', 'comments_list'))
