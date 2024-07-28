from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.db import transaction
from registration.forms import EmailUserCreationForm
from accounts.models import Profile
from registration.utils import send_confirmation_email


def signup(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                send_confirmation_email(request, user)
            messages.success(request, 'Please check your email to confirm your registration.')
            return redirect('login')
    else:
        form = EmailUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            login(request, user)
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            messages.success(request, 'Your email has been confirmed and your account is now active.')
            return redirect('edit_profile')
        else:
            messages.info(request, 'Your email has already been confirmed.')
            return redirect('login')
    else:
        messages.error(request, 'The confirmation link is invalid or has expired.')
        return render(request, 'registration/email_confirmation_failed.html')

