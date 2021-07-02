from django.urls import path

from Chat import views

urlpatterns = [
    path('', views.index),
    path('messages/<int:chat_id>', views.get_chat_messages)
]
