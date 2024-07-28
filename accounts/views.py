from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Follow, Profile
from accounts.forms import ProfileForm


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
    followers_count = user.followers.count()
    following_count = user.following.count()
    return render(request, 'accounts/profile.html', {
        'profile_user': user,
        'profile': profile,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect('feed')


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('feed')

@login_required
def user_search(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.none()
    return render(request, 'accounts/user_search_results.html', {'users': users})


@login_required
def friends_list(request):
    user = request.user
    friends = Follow.objects.filter(follower=user).select_related('followed')
    return render(request, 'accounts/friends_list.html', {'friends': friends})