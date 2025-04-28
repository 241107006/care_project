from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import Review, Order, SMSCode, CustomUser, Notification, Chat, Message, OrderTaken, PasswordCode
from .forms import ClientForm
import random
import string
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import os


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
        context = {
            'error': 'Неправильный логин или пароль'
        }
        return render(request, 'authorisation/login.html', context)
        

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

def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_email_with_gmail(subject, body, to_email):
    from_email = settings.EMAIL_HOST_USER 
    password = settings.EMAIL_HOST_PASSWORD
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_email, password)

        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def send_password_reset_email(email, code):
    subject = "Восстановления пароля"
    message = f"Ваша ссылка на восстановление пароля: http://zabotaplus.kz:8000/password_recovery/{code}"
    from_email = "no-reply@zabotaplus.kz"
    send_email_with_gmail(subject, message, email)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        user = CustomUser.objects.filter(email=email).first()
        # user = get_object_or_404(CustomUser, email=email)
        if not user:
            return render(request, 'authorisation/forgot_password.html', {'error': 'Почта не найдена'})
        PasswordCode.objects.filter(expiration__lt=timezone.now()).delete()
        
        code = generate_random_code()
        expiration_time = timezone.now() + timedelta(minutes=60)
        existing_code = PasswordCode.objects.filter(email=email).first()
        if existing_code:
            existing_code.code = code
            existing_code.save() 
        else:
            password_code = PasswordCode.objects.create(
                user=user,
                email=user.email,
                code=code,
                expiration=expiration_time
            )
        send_password_reset_email(user.email, code)
        
        return redirect('forgot_password_success', user.id)
    
    return render(request, 'authorisation/forgot_password.html')

def forgot_password_success(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'authorisation/forgot_password_success.html', {'email': user.email})

def password_recovery(request, code):
    PasswordCode.objects.filter(expiration__lt=timezone.now()).delete()
    context = {}
    rec_code = PasswordCode.objects.filter(code=code).first()
    if not rec_code:
        context['recovery_error'] = 'Срок действия кода восстановления пароля истек'
        return render(request, 'authorisation/password_recovery.html', context)
    if request.method == 'POST':
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        if not password or not password2:
            context['error'] = "Both password fields are required."
            return render(request, 'authorisation/password_recovery.html', context)
        if password != password2:
            context['error'] = "Passwords do not match."
            return render(request, 'authorisation/password_recovery.html', context)
        user = rec_code.user
        if not user:
            return redirect('home')
        
        rec_code.delete()
        user.set_password(password)
        user.save()
        
        return redirect('login')
    
    return render(request, 'authorisation/password_recovery.html')


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
        return render(request, 'my_orders.html', {'orders': orders, 'notifications_count': notifications_count(request)})
    orders_taken = OrderTaken.objects.filter(specialist=request.user).all()
    orders_list = []
    for order_taken in orders_taken:
        order = order_taken.order
        orders_list.append({
            'order': order,
            'order_taken': order_taken,
        })
    return render(request, 'my_taken_orders.html', {'orders': orders_list, 'notifications_count': notifications_count(request)})

def all_orderds(request):
    task_name = request.GET.get('task_name')
    if task_name:
        orders = Order.objects.filter(status='В ожидании', task_name=task_name).exclude(author=request.user)
    else:
        orders = Order.objects.filter(status='В ожидании').exclude(author=request.user)
    #<a href="{% url 'order_accept' order.id %}" class="btn btn-primary">Просмотреть</a>
    return render(request, 'all_orders.html', {'orders': orders, 'task_name': task_name})

def order_accept(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.user_type != 'Specialist':
        return redirect('home')
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return redirect('home')
    orderTaken = OrderTaken.objects.filter(order=order, specialist=request.user, client=order.author).first()
    if orderTaken:
        return redirect('order_detail', order_id=order.id)
    
    OrderTaken.objects.create(
        order=order,
        specialist=request.user,
        client=order.author,
    )
    
    # Send email to client
    subject = "Ваш заказ принят специалистом"
    message = f"""
    Здравствуйте, {order.author.full_name}!

    Специалист {request.user.full_name} принял ваш заказ "{order.task_name}".
    
    Детали заказа:
    - Название: {order.task_name}
    - Описание: {order.description}
    - Сроки: {order.deadline}
    - Оплата: {order.payment_min} - {order.payment_max} тенге
    
    Вы можете связаться со специалистом через чат на сайте.
    
    С уважением,
    Команда CARE+
    """
    send_email_with_gmail(subject, message, order.author.email)
    
    chat = Chat.objects.filter(
    (Q(user1=request.user, user2=order.author) | Q(user1=order.author, user2=request.user))).first()
    if not chat:
        chat = Chat.objects.create(user1=request.user, user2=order.author)
    Notification.objects.create(
        user = order.author,
        name = 'На вашу заявку откликнулись!',
        text = 'Перейдите по кнопке, чтобы связаться с специалистом',
        action = f'/chat/{chat.id}',
        action_name = 'Связаться'
    )
    return redirect('order_detail', order_id=order.id)

def order_finish(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    order = Order.objects.filter(id=order_id).first()
    if not order or order.author != request.user:
        return redirect('my_orders')
    order.status = 'Выполнено'
    order.save()
    return redirect('create_review', order.id)

def order_request_reject(request, request_id):
    if not request.user.is_authenticated:
        return redirect('login')
    order_request = OrderTaken.objects.filter(id=request_id).first()
    print(order_request.client, request.user)
    if not order_request or order_request.client != request.user:
        return redirect('chats')
    order_request.status = 'Отказано'
    order_request.save()
    
    chat = Chat.objects.filter(
    (Q(user1=request.user, user2=order_request.specialist) | Q(user1=order_request.specialist, user2=request.user))).first()
    print('isChat', chat)
    if chat:
        return redirect('chat', chat_id=chat.id)
    return redirect('chats')
    
def order_request_accept(request, request_id):
    if not request.user.is_authenticated:
        return redirect('login')
    order_request = OrderTaken.objects.filter(id=request_id).first()
    if not order_request or order_request.client != request.user:
        return redirect('chats')
    order = order_request.order
    if not order or order.status != 'В ожидании':
        return redirect('chats')
    order.status = 'Принято'
    order.save()
    
    order_request.status = 'Принято'
    order_request.save()
    
    # Send email to specialist
    subject = "Клиент принял ваш запрос"
    message = f"""
    Здравствуйте, {order_request.specialist.full_name}!

    Клиент {request.user.full_name} принял ваш запрос на выполнение заказа "{order.task_name}".
    
    Детали заказа:
    - Название: {order.task_name}
    - Описание: {order.description}
    - Сроки: {order.deadline}
    - Оплата: {order.payment_min} - {order.payment_max} тенге
    
    Вы можете связаться с клиентом через чат на сайте.
    
    С уважением,
    Команда CARE+
    """
    send_email_with_gmail(subject, message, order_request.specialist.email)
    
    chat = Chat.objects.filter(
    (Q(user1=order_request.specialist, user2=order.author) | Q(user1=order.author, user2=order_request.specialist))).first()
    if not chat:
        chat = Chat.objects.create(user1=order_request.specialist, user2=order.author)
    Notification.objects.create(
        user = order_request.specialist,
        name = 'Клиент принял запрос!',
        text = 'Перейдите по кнопке, чтобы связаться с клиентом',
        action = f'/chat/{chat.id}',
        action_name = 'Связаться'
    )
    
    requests = OrderTaken.objects.filter(order=order, status='В ожидании')
    for req in requests:
        req.status = 'Отказано'
        req.save()
    
    chat = Chat.objects.filter(
    (Q(user1=request.user, user2=order_request.specialist) | Q(user1=order_request.specialist, user2=request.user))).first()
    
    if chat:
        return redirect('chat', chat_id=chat.id)
    return redirect('chats')

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    action = request.GET.get('action')
    isMine = False
    no_review = False
    if request.user:
        isMine = order.author == request.user
    if isMine:
        review = Review.objects.filter(order=order).first()
        no_review = False if review else True
        if order.status != 'Выполнено':
            no_review = False
        no_review = True
    return render(request, 'order_detail.html', {'no_review': no_review, 'order': order, 'action': action, 'isMine': isMine})

def order_success(request, order_id):
    # If not my order redirect
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})

def read_notifications(user):
    notifications = Notification.objects.filter(user=user)
    for notification in notifications:
        notification.read = True
        notification.save()
        
def notifications_count(request):
    if not request.user.is_authenticated:
        return 0
    notifications = Notification.objects.filter(user=request.user, read=False)
    return notifications.count()
        
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
    return render(request, 'profile.html', {'document_is_pdf': document_is_pdf, 'notifications_count': notifications_count(request)})
    
def profile_view(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        return redirect('profile')
    print(user)
    reviews = Review.objects.filter(client=user_id)
    document_is_pdf = request.user.document and request.user.document.name.lower().endswith('.pdf')
    return render(request, 'profile_view.html', {'user': user, 'document_is_pdf': document_is_pdf, 'notifications_count': notifications_count(request), 'reviews': reviews})
    
def create_review(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    context = {}
    if not order:
        return redirect('my_orders')
    if order.author != request.user:
        return redirect('my_orders')
    if request.method == 'POST':
        text = request.POST['text']
        star = request.POST['star']
        Review.objects.create(
            order=order,
            client=request.user,
            text=text,
            star=star
        )
        return redirect('my_orders')
    context['order'] = order
    return render(request, 'create_review.html', context)
    
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
    return render(request, 'chats.html', {'chats': chat_list, 'notifications_count': notifications_count(request)})

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
    requests = OrderTaken.objects.filter(client=request.user, specialist=companion, status='В ожидании')
    print(requests)
    context = {
        'chats': chat_list,
        'current': chat,
        'messages': messages,
        'companion': companion,
        'requests': requests,
        'notifications_count': notifications_count(request)
    }
    
    return render(request, 'chat.html', context)

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notifications = Notification.objects.filter(user=request.user)
    print(notifications)
    read_notifications(request.user)
    return render(request, 'notifications.html', {'notifications': notifications})

