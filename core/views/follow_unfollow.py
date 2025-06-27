from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def follow(request, user_id):
    alvo = get_object_or_404(User, id=user_id)
    user = request.user

    if alvo != user:
        user.following.add(alvo)

    if alvo == request.user:
        return redirect('profile')
    else:
        return redirect('profileid', user_id=alvo.id)

@login_required
def unfollow(request, user_id):
    alvo = get_object_or_404(User, id=user_id)
    user = request.user

    if alvo != user:
        user.following.remove(alvo)

    if alvo == request.user:
        return redirect('profile')
    else:
        return redirect('profileid', user_id=alvo.id)