from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class CreateUserForm(UserCreationForm):
    username_validator = RegexValidator(r'[a-zA-Z0-9\s-]',
                                        'Используйте латиницу, цифры, пробелы или тире')

    name_validator = RegexValidator(r'[а-яА-Я\s-]',
                                        'Используйте кириллицу, пробелы или тире')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators.append(self.username_validator)
        for field in ['first_name', 'last_name']:
            self.fields[field].validators.append(self.name_validator)
        for field in ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CreateProfileForm(forms.ModelForm):
    patronymic_validator = RegexValidator(r'[а-яА-Я\s-]',
                                         'Используйте кириллицу, пробелы или тире')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patronymic'].validators.append(self.patronymic_validator)
        self.fields['rules'].required = True

    class Meta:
        model = UserProfile
        fields = ['patronymic', 'rules']


class LoginForm(AuthenticationForm):
    pass


class ReservationForm(forms.ModelForm):
    table = forms.ModelChoiceField(queryset=Table.objects.all(), empty_label=None)

    class Meta:
        model = Reservation
        fields = ['table', 'name', 'email', 'date', 'time']
        widgets = {
            'date': forms.DateInput(format=('%m/%d/%Y'), attrs={'type': 'date'}),
            'time': forms.TimeInput(format=('%H:%M'), attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        selected_table = cleaned_data.get('table')

        if date and time and selected_table:
            # Преобразуем дату и время в datetime
            start_time = datetime.combine(date, time)
            end_time = start_time + timedelta(hours=1)

            # Проверяем наличие конфликта бронирования
            existing_reservations = Reservation.objects.filter(
                table=selected_table,
                date=date,
                time__range=(start_time.time(), end_time.time())
            )

            if existing_reservations.exists():
                raise forms.ValidationError("Извините, этот столик уже забронирован на выбранное время.")

        return cleaned_data


class FoodReservationForm(forms.ModelForm):
    class Meta:
        model = FoodReservation
        fields = ['product', 'quantity', 'date']
        widgets = {
            'date': forms.DateInput(format=('%m/%d/%Y'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()