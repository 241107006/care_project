from django import forms

class ClientForm(forms.Form):
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
        label="Введите что нужно сделать",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_task_name_input'}),
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
        label="Напишите особенности здоровья",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_health_issues_input', 'style': 'display: none;'}),
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
        label="Другое",
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
        label="Другое",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_frequency_input', 'style': 'display: none;'}),
    )
    
    WORKING_HOURS_CHOICES = [
        ('Несколько часов в день', 'Несколько часов в день'),
        ('Полный день', 'Полный день'),
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
        label="Другое",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_working_hours_input', 'style': 'display: none;'}),
    )    
    start_date = forms.DateField(label="Когда нужна услуга", required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    address = forms.CharField(label="Адрес выполнения работы", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    payment_min = forms.DecimalField(label="Минимальная оплата", required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    payment_max = forms.DecimalField(label="Максимальная оплата", required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    additional_notes = forms.CharField(label="Пожелания к заказу", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    phone = forms.CharField(label="Номер телефона", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label="Имя и фамилия клиента", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

