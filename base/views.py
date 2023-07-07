from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, EditRoomForm, MyUserCreationForm, UserForm

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Invalid email/password')
            return redirect('login')
    page = 'login'
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        try:
            if form.is_valid:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
        except:
            messages.error(request, 'PLEASE TRY AGAIN')
            return redirect('register')

    context = {'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(user__username__icontains=q)
    )
    topics = Topic.objects.all()
    roomCount = Room.objects.all().count
    activityMessages = Message.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'roomCount':roomCount,
               'activityMessages':activityMessages}
    return render(request,'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    roomCount = Room.objects.all().count
    roomMessages = room.message_set.all()

    if request.method == 'POST':
        Message.objects.create(
            room = room,
            user = request.user,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    participants = room.participants.all()
    context = {'room':room, 'topics':topics, 'roomCount':roomCount, 'participants':participants,
               'roomMessages':roomMessages}
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm
    topics = Topic.objects.all()
    if request.method == 'POST':
        topicName = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topicName)
        room = Room.objects.create(
            topic = topic,
            user = request.user,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        room.participants.add(request.user)
        return redirect('home')
    page = 'create'
    context = {'form':form, 'topics':topics, 'page':page}
    return render(request,'base/room_form.html', context)

@login_required(login_url='/login')
def editRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = EditRoomForm(instance=room)
    page = 'edit'

    if request.user != room.user:
        return HttpResponse('YOU ARE NOT ALLOWED HERE')

    if request.method == 'POST':
        form = EditRoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('room', pk=room.id)

    context = {'form':form, 'page':page, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.user:
        return HttpResponse('YOU ARE NOT ALLOWED HERE!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('YOU ARE NOT ALLOWED HERE')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    activityMessages = user.message_set.all()
    roomCount = Room.objects.all().count
    context = {'user':user, 'topics':topics, 'rooms':rooms, 'activityMessages':activityMessages,
               'roomCount':roomCount}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def editProfile(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid:
            info = form.save(commit=False)
            info.username = info.username.lower()
            info.save()
            return redirect('profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/editProfile.html', context)

def activitiesPage(request):
    activityMessages = Message.objects.all()
    context = {'activityMessages':activityMessages}
    return render(request, 'base/activity.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    return render(request, 'base/topics.html',{'topics':topics})
