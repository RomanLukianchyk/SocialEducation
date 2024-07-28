from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import PostForm
from blog.models import Post, Tag, PostTag, Like, Dislike
from accounts.models import Follow


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            tags = form.cleaned_data.get('tags', '')
            if tags:
                tag_names = [tag.strip() for tag in tags.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    PostTag.objects.create(post=post, tag=tag)

            return redirect('feed')
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    user = request.user
    following = Follow.objects.filter(follower=user).values_list('followed', flat=True)

    for post in posts:
        post.likes_count = Like.objects.filter(post=post).count()
        post.dislikes_count = Dislike.objects.filter(post=post).count()

    return render(request, 'blog/feed.html', {'posts': posts, 'following': following})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('feed')


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    dislike, created = Dislike.objects.get_or_create(user=request.user, post=post)
    if not created:
        dislike.delete()
    return redirect('feed')

@login_required
def friends_feed(request):
    user = request.user
    friends = Follow.objects.filter(follower=user).values_list('followed', flat=True)
    posts = Post.objects.filter(author__in=friends).order_by('-created_at')

    for post in posts:
        post.likes_count = Like.objects.filter(post=post).count()
        post.dislikes_count = Dislike.objects.filter(post=post).count()

    return render(request, 'blog/friends_feed.html', {'posts': posts})
