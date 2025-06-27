from django.shortcuts import render, redirect
from django.db.models import OuterRef, Subquery, DateTimeField, CharField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from ..utils import get_or_create_private_chat
from ..models import Organizacao, CustomUser, ChatRoom, Message


def load_more_messages(request, room_name):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Usuário não autenticado'}, status=403)

        page = int(request.GET.get('page', 1))

        ids = [int(x) for x in room_name.split('_')]
        room = None
        all_rooms = ChatRoom.objects.filter(is_group=False, participants=request.user)

        for r in all_rooms:
            participantes = list(r.participants.values_list('id', flat=True))
            if sorted(participantes) == sorted(ids):
                room = r
                break

        if not room:
            return JsonResponse({'error': 'Sala não encontrada'}, status=404)

        messages_qs = room.messages.all().order_by('-timestamp')
        paginator = Paginator(messages_qs, 15)
        page_obj = paginator.page(page)

        messages_data = [
            {
                'content': msg.content,
                'sender': msg.sender.email,
                'timestamp': msg.timestamp.strftime('%H:%M'),
            }
            for msg in reversed(page_obj.object_list)
        ]

        return JsonResponse({
            'messages': messages_data,
            'has_more': page_obj.has_next()
        })

    except Exception as e:
        import traceback
        print("ERRO AO CARREGAR MENSAGENS:", e)
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

class ChatView(TemplateView):
    template_name = "chat.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_user')

        if not Organizacao.objects.filter(deleted_at__isnull=True, membros=request.user).exists():
                return redirect('create-organization')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_destino_id = self.kwargs.get('user_id')

        get_last_msg = Message.objects.filter(
            room=OuterRef('pk')
        ).order_by('-timestamp').values('timestamp')[:1]


        if user_destino_id:
            user_destino = get_object_or_404(CustomUser, id=user_destino_id)
            room = get_or_create_private_chat(self.request.user, user_destino)

            messages_qs = room.messages.all().order_by('-timestamp')
            paginator = Paginator(messages_qs, 15)
            first_page = paginator.page(1)

            context['room_name'] = room.get_room_name()
            context['messages'] = reversed(first_page.object_list)
            context['has_more'] = first_page.has_next()
            context['selected_user'] = user_destino
        else:
            context['room_name'] = ''
            context['messages'] = []
            context['selected_user'] = None

        context['membros'] = CustomUser.objects.exclude(id=self.request.user.id)
        context['chats'] = (
            ChatRoom.objects
            .filter(participants=self.request.user)
            .annotate(
                ultima_msg_data=Subquery(get_last_msg.values('timestamp')[:1], output_field=DateTimeField()),
                ultima_msg_texto=Subquery(get_last_msg.values('content')[:1], output_field=CharField())
            )
            .order_by('-ultima_msg_data', '-created_at')
            .prefetch_related('participants')
        )
        return context