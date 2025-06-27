from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from ..models import Organizacao, Grupo, Post, Like, CustomUser

class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')  # Redireciona se o usuário não estiver logado

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()
        groups = Grupo.objects.filter(deleted_at__isnull=True, membros=request.user, organizacao=organization)
        posts = Post.objects.filter(deleted_at__isnull=True, grupo__in=groups).order_by('-created_at')
        users = CustomUser.objects.filter(membros_organizacao__id = organization.id).exclude(id=self.request.user.id)

        for post in posts:
            post.is_liked = post.likes.filter(user=request.user).exists()

        context = {
            'organization': organization,
            'posts':posts,
            'groups': groups,
            'users':users,
        }

        return render(request, 'index.html', context)

    def post(self, request):
        user = request.user

        if "like-post-btn" in request.POST:
            post_id = request.POST.get("post-id")
            group_id = request.POST.get("group-id")
            post = get_object_or_404(Post, id=post_id)
            print(f'{post_id}, {group_id}, {post}')

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                try:
                    like, created = Like.objects.get_or_create(user=user, post=post)

                    if not created:
                        like.delete()
                        liked = False
                    else:
                        liked = True

                    return JsonResponse({
                        "likes": post.likes.count(),
                        "liked": liked
                    })
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=400)

            return JsonResponse({"error": "Requisição inválida"}, status=400)

        return redirect('group-detail', id=id)