from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom
from .forms import ChatForm

# Create your views here.


@login_required
def chat_list(request):
    current_user_id = request.user.personal_id
    list_of_rooms = ChatRoom.objects.all().filter(allowed_users__personal_id=current_user_id)
    return render(request, 'chat/chat_list.html', locals())


@login_required
def chat_add(request):
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            #adding person creating room to allowed users
            chat.allowed_users.add(request.user.personal_id)
            chat.save()
            return redirect('/')
    else:
        form = ChatForm()
    return render(request, 'chat/chat_form.html', {'form': form})


@login_required
def chat_view(request, pk):
    room = get_object_or_404(ChatRoom, pk=pk)
    return render(request, 'chat/chat_room.html', locals())