import json

from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from Pydate.models import Match


@receiver(post_save, sender=Match)
def after_match(sender, instance, **kwargs):
    if instance.personal_questions_match == '11':
        user1 = instance.user1
        user2 = instance.user2
        chats = UserChat.objects.filter(user=user1)
        # ids = [c.chat for c in chats]
        # if len(possible) == 0:
        chat = Chat()
        chat.save()
        UserChat(chat=chat, user=user1).save()
        UserChat(chat=chat, user=user2).save()


class Chat(models.Model):
    chatID = models.AutoField(primary_key=True)
    # date = models.DateField(auto_now=True)
    agreement = models.IntegerField(default=1)


class UserChat(models.Model):
    userChatID = models.AutoField(primary_key=True, unique=True)
    chat = models.ForeignKey(Chat, unique=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)

    @staticmethod
    def user_belongs_to(user, chat_id):
        return UserChat.objects.filter(chat=chat_id, user=user)

    @staticmethod
    @database_sync_to_async
    def get_available_chats(user):
        return [i.chat.chatID for i in list(UserChat.objects.filter(user=user))]

    @staticmethod
    def chats_info(user):
        result = []
        for i in list(UserChat.objects.filter(user=user)):
            temp = {
                "chat_id": i.chat.chatID,
                "username": list(UserChat.objects.filter(chat=i.chat).exclude(user=user))[0].user.username
            }
            result.append(temp)
        return result


class ChatMessage(models.Model):
    messageID = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, unique=False, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.message = self.message.strip()
        super(ChatMessage, self).save(*args, **kwargs)

    @staticmethod
    @database_sync_to_async
    def save_message(username, chat_id, message):
        user = list(User.objects.filter(username=username))[0]
        chat = Chat.objects.get(chatID=chat_id)
        mes = ChatMessage(user=user, chat=chat, message=message)
        mes.save()
        return mes.date

    @staticmethod
    def get_latest(chat_id, start, end):
        chat = Chat.objects.get(chatID=chat_id)
        mes_list = list(ChatMessage.objects.filter(chat=chat).order_by('-date'))
        end = min(max(end, 0), len(mes_list))
        start = max(start, 0)
        mes_list = mes_list[start:end]
        json_list = []
        for i in mes_list[::-1]:
            temp = {
                "type": "MESSAGE",
                "chat_id": i.chat.chatID,
                "username": i.user.username,
                "message": i.message,
                "date": json.dumps(i.date, cls=DjangoJSONEncoder)
            }
            json_list.append(temp)
        return json_list
