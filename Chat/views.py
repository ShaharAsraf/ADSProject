from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from Chat.models import UserChat, ChatMessage


@login_required
def index(request):
    user = request.user
    chats = UserChat.chats_info(user)
    return render(request, 'index.html', {'chats': chats, 'username': user.username})


@login_required
def get_chat_messages(request, chat_id):
    if UserChat.user_belongs_to(request.user, chat_id):
        messages = ChatMessage.get_latest(chat_id, 0, 20)
        return JsonResponse({'messages': messages})
    else:
        return JsonResponse(status=400)
