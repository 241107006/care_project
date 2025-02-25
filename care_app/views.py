from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import Order, SMSCode, CustomUser, Notification, Chat, Message, OrderTaken
from .forms import ClientForm
import random
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def create_code():
    return str(random.randint(100000, 999999))

def login_view(request):
    if request.method == 'GET':
        return render(request, 'authorisation/login.html')
    if request.method == 'POST':
        print(request.POST)
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if not phone or not password:
            return redirect('login')
        user = authenticate(request, phone=phone, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        return redirect('login')
        

def register_view(request):
    try:
        step = int(request.POST.get('step', 1))
    except ValueError:
        step = 1

    context = {
        'step': step,
        'isSpecialist': request.POST.get('isSpecialist', 'no'),
        'phone': request.POST.get('phone', ''),
        'email': request.POST.get('email', ''),
        'name': request.POST.get('name', ''),
        'birthday': request.POST.get('birthday', ''),
        'sex': request.POST.get('sex', ''),
    }
    print(context)
    
    if request.method == 'GET':
        # if step == 2 and context['phone']:
        #     code = SMSCode.objects.filter(phone=context['phone']).order_by('-created_at').first()
        #     context['code'] = code
        return render(request, 'authorisation/register.html', context)
    
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        birthday = request.POST.get('birthday', '')
        sex = request.POST.get('sex', '')
        isSpecialist = request.POST.get('isSpecialist', 'no')
        
        if step == 1:
            print('step 1', phone, email)
            # Step 1: Collect phone and email.
            if not phone or not email:
                context['error'] = "Phone and email are required."
                return render(request, 'authorisation/register.html', context)
            
            if CustomUser.objects.filter(phone=phone).exists():
                context['error'] = 'Phone already in use'
                context['phone'] = ''
                return render(request, 'authorisation/register.html', context)
            if CustomUser.objects.filter(email=email).exists():
                context['error'] = 'Email already in use'
                context['email'] = ''
                return render(request, 'authorisation/register.html', context)
            
            context['step'] = 3
            return render(request, 'authorisation/register.html', context)
        
        elif step == 2:
            # Step 2: For example, OTP verification could be handled here.
            # We assume OTP verification is done and move to step 3.
            return render(request, 'authorisation/register.html', context)
        
        elif step == 3:
            # If previous data not fully provided return by steps
            if not phone or not email:
                context['step'] = 1
                context['error'] = "Phone and email are required."
                return render(request, 'authorisation/register.html', context)
            if CustomUser.objects.filter(phone=phone).exists():
                context['error'] = 'Phone already in use'
                context['step'] = 1
                context['phone'] = ''
                return render(request, 'authorisation/register.html', context)
            if CustomUser.objects.filter(email=email).exists():
                context['error'] = 'Email already in use'
                context['step'] = 1
                context['email'] = ''
                return render(request, 'authorisation/register.html', context)
            
            # Step 3: Collect additional information (name, birthday, sex).
            if not name or not birthday or not sex:
                context['error'] = "Name, birthday, and gender are required."
                return render(request, 'authorisation/register.html', context)
            
            context['step'] = 4
            return render(request, 'authorisation/register.html', context)
        
        elif step == 4:
            # If previous data not fully provided return by steps
            if not phone or not email:
                context['step'] = 1
                context['error'] = "Phone and email are required."
                return render(request, 'authorisation/register.html', context)
            if CustomUser.objects.filter(phone=phone).exists():
                context['error'] = 'Phone already in use'
                context['step'] = 1
                context['phone'] = ''
                return render(request, 'authorisation/register.html', context)
            if CustomUser.objects.filter(email=email).exists():
                context['error'] = 'Email already in use'
                context['step'] = 1
                context['email'] = ''
                return render(request, 'authorisation/register.html', context)
            if not name or not birthday or not sex:
                context['error'] = "Name, birthday, and gender are required."
                context['step'] = 3
                return render(request, 'authorisation/register.html', context)
            
            # Step 4: Password creation.
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            
            if not password or not password2:
                context['error'] = "Both password fields are required."
                return render(request, 'authorisation/register.html', context)
            
            if password != password2:
                context['error'] = "Passwords do not match."
                return render(request, 'authorisation/register.html', context)
            
            user_type = 'Specialist' if isSpecialist == 'yes' else 'Client'
            print(user_type)
            user = CustomUser.objects.create_user(
                phone=phone,
                email=email,
                name=name,
                birthday=birthday,
                sex=sex,
                password=password,
                user_type=user_type,
            )
            
            return redirect('login')
    
    return render(request, 'authorisation/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def create_order(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            if form.cleaned_data['other_task_name']:
                task_name = form.cleaned_data['other_task_name']
            order = Order.objects.create(
                author=request.user,
                task_name=task_name,
                help_for=form.cleaned_data['help_for'],
                gender=form.cleaned_data['gender'],
                age=form.cleaned_data['age'],
                weight=form.cleaned_data['weight'],
                height=form.cleaned_data['height'],
                health_issues=form.cleaned_data['health_issues'],
                mobility=form.cleaned_data['mobility'],
                care_location=form.cleaned_data['care_location'],
                frequency=form.cleaned_data['frequency'],
                working_hours=form.cleaned_data['working_hours'],
                start_date=form.cleaned_data['start_date'],
                address=form.cleaned_data['address'],
                payment_min=form.cleaned_data['payment_min'],
                payment_max=form.cleaned_data['payment_max'],
                additional_notes=form.cleaned_data['additional_notes'],
                phone=form.cleaned_data['phone'],
                full_name=form.cleaned_data['full_name']
            )
            return redirect('order_success', order_id=order.id)
    else:
        form = ClientForm()
    task_name = request.GET.get('task_name')
    return render(request, 'create_order.html', {'form': form, 'task_name': task_name})

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.user_type == 'Client':
        orders = Order.objects.filter(author=request.user)
        return render(request, 'my_orders.html', {'orders': orders})
    orders_taken = OrderTaken.objects.filter(specialist=request.user).all()
    orders_list = []
    for order_taken in orders_taken:
        order = order_taken.order
        orders_list.append({
            'order': order,
            'order_taken': order_taken,
        })
    return render(request, 'my_taken_orders.html', {'orders': orders_list})

def all_orderds(request):
    orders = Order.objects.filter(status='В ожидании').exclude(author=request.user)
    #<a href="{% url 'order_accept' order.id %}" class="btn btn-primary">Просмотреть</a>
    return render(request, 'all_orders.html', {'orders': orders})

def order_accept(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.user_type != 'Specialist':
        return redirect('home')
    order = get_object_or_404(Order, id=order_id)
    OrderTaken.objects.create(
        order=order,
        specialist=request.user,
    )
    order.status = 'Принято'
    order.save()
    chat = Chat.objects.filter(
    (Q(user1=request.user, user2=order.author) | Q(user1=order.author, user2=request.user))).first()
    if not chat:
        chat = Chat.objects.create(user1=request.user, user2=order.author)
    Notification.objects.create(
        user = order.author,
        name = 'На вашу заявку откликнулись!',
        text = 'Перейдите по кнопке, чтобы связаться с клиентом',
        action = f'/chat/{chat.id}',
        action_name = 'Связаться'
    )
    return redirect('order_detail', order_id=order.id)

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    action = request.GET.get('action')
    isMine = False
    if request.user:
        isMine = order.author == request.user
    return render(request, 'order_detail.html', {'order': order, 'action': action, 'isMine': isMine})

def order_success(request, order_id):
    # If not my order redirect
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})

def read_notifications(user):
    notifications = Notification.objects.filter(user=user)
    for notification in notifications:
        notification.read = 'read'
        notification.save()
        
@csrf_exempt
@login_required
def send_message(request, chat_id):
    print('request', request)
    if request.method == 'POST':
        chat = Chat.objects.filter(id=chat_id).first()
        if not chat or (chat.user1 != request.user and chat.user2 != request.user):
            return JsonResponse({'status': 'error', 'message': 'Invalid chat'}, status=400)

        message_text = request.POST.get('text', '')
        message_file = request.FILES.get('file', None)
        if not message_text and not message_file:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'}, status=400)

        Message.objects.create(
            chat_id=chat,
            sender=request.user,
            text=message_text,
            file=message_file
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
       
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        photo = request.FILES.get('photo')
        document = request.FILES.get('document')
        
        user = request.user
        if name:
            user.name = name
        if surname:
            user.surname = surname
        if gender and gender in ('Male', 'Female'):
            user.sex = gender
        if phone:
            user.phone = phone
        if birthday:
            user.birthday = birthday
        if photo:
            user.profile_picture = photo
        if document:
            user.document = document
        user.save()
    # notifications
    document_is_pdf = request.user.document and request.user.document.name.lower().endswith('.pdf')
    return render(request, 'profile.html', {'document_is_pdf': document_is_pdf})
    
    
def chats(request):
    if not request.user.is_authenticated:
        return redirect('login')
    chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    chat_list = []
    for chat in chats:
        other_user = chat.user2 if chat.user1 == request.user else chat.user1
        last_message = Message.objects.filter(chat_id=chat).order_by('created_at').last()
        chat_list.append({
            'chat': chat,
            'other_user': other_user,
            'last_message': last_message,
        })
    return render(request, 'chats.html', {'chats': chat_list})

def chat(request, chat_id):
    if not request.user.is_authenticated:
        return redirect('login')
    chat = Chat.objects.filter(id=chat_id).first()
    if not chat or (chat.user1 != request.user and chat.user2 != request.user):
        return HttpResponse("Invalid chat<br><a href='/'>Home</a>", status=400)
    
    chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    chat_list = []
    for chati in chats:
        other_user = chati.user2 if chati.user1 == request.user else chati.user1
        last_message = Message.objects.filter(chat_id=chati).order_by('created_at').last()
        chat_list.append({
            'chat': chati,
            'other_user': other_user,
            'last_message': last_message,
        })
    messages = Message.objects.filter(chat_id=chat)
    companion = chat.user1 if request.user == chat.user2 else chat.user2
    return render(request, 'chat.html', {'chats': chat_list, 'current': chat, 'messages': messages, 'companion': companion})

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('login')
    '''Notification.objects.create(
        user=request.user,
        name = 'На вашу заявку откликнулись!', 
        text = 'Перейдите по кнопке, чтобы связаться с клиентом',
        action = '/chat/1',
        action_name = 'Связаться '
    )'''
    notifications = Notification.objects.filter(user=request.user)
    read_notifications(request.user)
    return render(request, 'notifications.html', {'notifications': notifications})

