from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from ..models import Organizacao, Grupo, Post, Like
from ..forms import GroupForm

class GroupView(TemplateView):
    template_name = "groups.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()
        groups = Grupo.objects.filter(deleted_at__isnull=True, membros=request.user, organizacao=organization)
        add_form = GroupForm()

        context = {
            'organization': organization,
            'groups': groups,
            'add_form': add_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST, request.FILES)

        if form.is_valid():
            group = form.save(user=request.user)
            return redirect('group')

        organization = Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).first()
        groups = Grupo.objects.filter(deleted_at__isnull=True, membros=request.user, organizacao=organization)

        context = {
            'organization': organization,
            'groups': groups,
            'add_form': form,
        }
        return render(request, self.template_name, context)

class GroupDetailView(TemplateView):
    template_name = "groups.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')  # Redireciona se o usuário não estiver logado

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
            return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        group = get_object_or_404(Grupo, id=id)
        membersCount = Grupo.membros.through.objects.filter(grupo_id = id)
        posts = Post.objects.filter(deleted_at__isnull=True, grupo=group).order_by('-created_at')

        for post in posts:
            post.is_liked = post.likes.filter(user=request.user).exists()

        context = {
            'group': group,
            'membersCount': membersCount,
            'posts': posts,
        }

        return render(request, 'group-details.html', context)

    def post(self, request, id):
        group = get_object_or_404(Grupo, id=id)
        user = request.user

        if "create-post-btn" in request.POST:
            titulo = request.POST.get("title-post")
            grupo = group
            autor = user
            conteudo = request.POST.get("message-post")

            try:
                Post.objects.create(
                    titulo=titulo,
                    grupo=grupo,
                    autor=autor,
                    conteudo=conteudo,
                )

                return redirect('group-detail', id=id)
            except Exception as e:
                print(f"Erro ao criar Postagem: {e}")

        elif "like-post-btn" in request.POST:
            post_id = request.POST.get("post-id")
            post = get_object_or_404(Post, id=post_id)

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