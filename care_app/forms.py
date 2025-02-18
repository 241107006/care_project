from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from .models import Order

class ClientForm(forms.Form):
    DAYS_OF_WEEK = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]
    
    HOURS_PERIOD = [
        ('Утро', 'Утро (08:00 - 12:00)'),
        ('День', 'День (12:00 - 16:00)'),
        ('Вечер', 'Вечер (16:00 - 20:00)'),
        ('Ночь', 'Ночь (20:00 - 08:00)'),
    ]
    
    TASK_NAME_CHOICES = [
            ('Гигиенические процедуры', 'Гигиенические процедуры'),
            ('Кормить', 'Кормить'),
            ('Готовить еду', 'Готовить еду'),
            ('Помогать по хозяйству', 'Помогать по хозяйству'),
            ('Выполнять медицинские назначения', 'Выполнять медицинские назначения'),
            ('Менять памперсы', 'Менять памперсы'),
            ('Сопровождать на прогулку', 'Сопровождать на прогулку'),
            ('Сопровождать в медицинские учреждения', 'Сопровождать в медицинские учреждения'),
            ('Другое', 'Другое'),
    ]
    task_name = forms.ChoiceField(
        choices=TASK_NAME_CHOICES,
        label="Как назвать задачу",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange':'showOtherInput(this, "other_task_name_input")'}),
    )
    other_task_name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_task_name_input', 'placeholder': 'Введите что нужно сделать'}),
    )


    HELP_FOR = [
        ('Мне', 'Мне'),
        ('Другому человеку', 'Другому человеку'),
    ]
    help_for = forms.ChoiceField(
        label="Кому нужна помощь?",  
        choices=HELP_FOR, 
        widget=forms.Select(attrs={'class': 'form-control'}))

    GENDER_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]
    gender = forms.ChoiceField(
        label="Пол клиента", 
        choices=GENDER_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}))

    age = forms.IntegerField(label="Возраст", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(label="Вес (кг)", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.FloatField(label="Рост (см)", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    HEALTH_ISSUES = [
        ('Деменция', 'Деменция'),
        ('Инсульт', 'Инсульт'),
        ('Онкология', 'Онкология'),
        ('Перелом шейки бедра', 'Перелом шейки бедра'),
        ('Болезнь Альцгеймера', 'Болезнь Альцгеймера'),
        ('Сахарный диабет', 'Сахарный диабет'),
        ('ДЦП','ДЦП'),
        ('Рассеянный склероз','Рассеянный склероз'),
        ('Послеоперационный период','Послеоперационный период'),
        ('Другое','Другое'),

    ]
    health_issues = forms.ChoiceField(
        label="Есть особенности здоровья", 
        choices=HEALTH_ISSUES, 
        widget=forms.Select(attrs={'class': 'form-control', 'onchange':'showOtherInput(this, "other_health_issues_input")'}),
    )
    other_health_issues = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_health_issues_input', 'style': 'display: none;', 'placeholder': 'Напишите особенности здоровья'}),
    )


    MOBILITY_CHOICES = [
        ('Самостоятельно', 'Самостоятельно'),
        ('С трудом', 'С трудом'),
        ('На коляске', 'На коляске'),
        ('С помощью ходунков', 'С помощью ходунков'),
        ('Нет','Нет')
    ]
    mobility = forms.ChoiceField(
        label="Как передвигается?",
        choices=MOBILITY_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}))

    
    CARE_LOCATION_CHOICES = [
        ('Дома у клиента', 'Дома у клиента'),
        ('В больнице(общая палата)', 'В больнице(общая палата)'),
        ('В больнице(частная палата)','В больнице(частная палата)'),
        ('Другое','Другое')
    ]
    care_location = forms.ChoiceField(
        label="Где выполнять уход", 
        choices=CARE_LOCATION_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control', 'onchange':'showOtherInput(this, "other_location_input")'}),)
    other_location = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_location_input', 'style': 'display: none;'}),
    )

    FREQUENCY_CHOICES = [
        ('На постоянной основе без проживания', 'На постоянной основе без проживания'),
        ('На постоянной основе с проживанием', 'На постоянной основе с проживанием'),
        ('Несколько раз в неделю', 'Несколько раз в неделю'),
        ('На один раз','На один раз'),
        ('Другое','Другое')
    ]
    frequency = forms.ChoiceField(
        label="Как часто нужна помощь?", 
        choices=FREQUENCY_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control', 'onchange':'showOtherInput(this, "other_frequency_input")'}),
    )
    other_frequency = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_frequency_input', 'style': 'display: none;'}),
    )
    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="",   
    )
    
    WORKING_HOURS_CHOICES = [
        ('Полный день', 'Полный день'),
        ('Несколько часов в день', 'Несколько часов в день'),
        ('Круглосуточно', 'Круглосуточно'),
        ('Только ночью', 'Только ночью'),
        ('Другое','Другое')
    ]
    working_hours = forms.ChoiceField(
        label="Время работы", 
        choices=WORKING_HOURS_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control', 'onchange':'showOtherInput(this, "other_working_hours_input")'}),)
    other_working_hours = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_working_hours_input', 'style': 'display: none;'}),
    )
    hours_period = forms.MultipleChoiceField(
        choices=HOURS_PERIOD,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="",
    )
    
    
    start_date = forms.DateField(label="Когда нужна услуга", required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    address = forms.CharField(label="Адрес выполнения работы", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    payment_min = forms.DecimalField(label="Минимальная оплата", required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    payment_max = forms.DecimalField(label="Максимальная оплата", required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    additional_notes = forms.CharField(label="Пожелания к заказу", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    phone = forms.CharField(label="Номер телефона", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label="Имя и фамилия клиента", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'frequency': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleFields()'}),
            'working_hours': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleFields()'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get("frequency")
        working_hours = cleaned_data.get("working_hours")
        days_of_week = cleaned_data.get("days_of_week")
        hours_period = cleaned_data.get("hours_period")
        start_date = cleaned_data.get("start_date")

        if frequency == 'Несколько раз в неделю':
            if not days_of_week:
                self.add_error("days_of_week", "Выберите хотя бы один день недели.")
            cleaned_data["frequency"] = ", ".join(days_of_week) if days_of_week else frequency
        
        if working_hours == 'Несколько часов в день':
            if not hours_period:
                self.add_error("hours_period", "Выберите хотя бы один период времени.")
            cleaned_data["working_hours"] = ", ".join(hours_period) if hours_period else working_hours
        
        if start_date and start_date < date.today():
            self.add_error("start_date", "Дата должна быть в будущем.")
            
        return cleaned_data
