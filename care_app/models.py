from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator

class Order(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    task_name = models.CharField(max_length=255, verbose_name="Название задачи")
    help_for = models.CharField(max_length=50, verbose_name="Кому нужна помощь?")
    gender = models.CharField(max_length=10, verbose_name="Пол клиента")
    age = models.PositiveIntegerField(verbose_name="Возраст", null=True, blank=True)
    weight = models.FloatField(verbose_name="Вес (кг)", null=True, blank=True)
    height = models.FloatField(verbose_name="Рост (см)", null=True, blank=True)

    # Особенности здоровья
    health_issues = models.TextField(verbose_name="Особенности здоровья", blank=True, null=True)

    # Передвижение
    mobility = models.CharField(max_length=50, verbose_name="Как передвигается?", blank=True)

    # Где выполнять уход
    care_location = models.CharField(max_length=50, verbose_name="Место ухода", blank=True)

    # Частота и время
    frequency = models.CharField(max_length=100, verbose_name="Как часто нужна помощь?", blank=True)
    working_hours = models.CharField(max_length=100, verbose_name="Время работы", blank=True)

    # Сроки и адрес
    start_date = models.DateField(verbose_name="Когда нужна услуга", blank=True, null=True)
    address = models.TextField(verbose_name="Адрес выполнения работы", blank=True)

    # Оплата
    payment_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Минимальная оплата", null=True, blank=True)
    payment_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Максимальная оплата", null=True, blank=True)

    # Пожелания
    additional_notes = models.TextField(verbose_name="Пожелания к заказу", blank=True)
    
    # Контакты
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    full_name = models.CharField(max_length=100, verbose_name="Имя и фамилия клиента")

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=40, 
        verbose_name="Статус",
        choices=[
            ('В ожидании', 'В ожидании'),
            ('Принято', 'Принято'),
            ('Выполнено', 'Выполнено'),
        ],
        default='В ожидании'
    )
    
class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, name, surname, birthday, sex, password=None):
        if not phone:
            raise ValueError("The Phone field is required.")
        if not email:
            raise ValueError("The Email field is required.")

        email = self.normalize_email(email)
        user = self.model(
            phone=phone,
            email=email,
            name=name,
            surname=surname,
            birthday=birthday,
            sex=sex,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, name, surname, birthday, sex, password=None):
        user = self.create_user(
            phone=phone,
            email=email,
            name=name,
            surname=surname,
            birthday=birthday,
            sex=sex,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    TYPE_CHOICES = [
        ('Specialist', 'Specialist'),
        ('Client', 'Client'),
    ]

    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthday = models.DateField()
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    user_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.FileField(upload_to='profile_pictures/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpeg','jpg','png'])])
    document = models.FileField(upload_to='documents/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpeg','jpg','png', 'pdf'])])

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'name', 'surname', 'birthday', 'sex']

    def __str__(self):
        return f"{self.name} {self.surname} ({self.phone})"
    
class SMSCode(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    name = models.TextField()
    text = models.TextField()
    action = models.TextField()
    action_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Chat(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_as_user1', null=True, blank=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_as_user2', null=True, blank=True)
    class Meta:
        unique_together = ('user1', 'user2')
    
class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    text = models.TextField()
    file = models.FileField(upload_to='message_files/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpeg','jpg','png'])])
    read = models.CharField(max_length=6, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    
class OrderTaken(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='taken_orders')
    specialist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='taken_orders')

    # = models.OneToOneField(Model, on_delete=models.CASCADE, related_name='')
    # = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='')