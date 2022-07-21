from django.shortcuts import render


def main_chat_page(request):
    return render(request, 'chat/chat_main.html')


def room_page(request, room_name):
    return render(request, 'chat/room_page.html', {
        'room_name': room_name,
    })
