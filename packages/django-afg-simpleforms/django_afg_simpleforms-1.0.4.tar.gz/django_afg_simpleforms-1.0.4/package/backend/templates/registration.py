<!DOCTYPE html>#}
{#<html lang="en">#}
{#<head>#}
{#    <meta charset="UTF-8">#}
{#    <style>#}
{#        .error {#}
{#            color: red;#}
{#            margin-top: 5px;#}
{#        }#}
{#    </style>#}
{#</head>#}
{#<body>#}
{#    <form method="POST" action="" id="registration-form">#}
{#        {% csrf_token %}#}
{#        <div>#}
{#            {{ user_form.first_name.label }}:#}
{#            {{ user_form.first_name }}#}
{#            <div class="error" id="first-name-error"></div>#}
{#        </div>#}
{#        <div>#}
{#            {{ user_form.last_name.label }}:#}
{#            {{ user_form.last_name }}#}
{#            <div class="error" id="last-name-error"></div>#}
{#        </div>#}
{#        <div>#}
{#            {{ profile_form.patronymic.label }}:#}
{#            {{ profile_form.patronymic }}#}
{#            <div class="error" id="patronymic-error"></div>#}
{#        </div>#}
{#        <div>#}
{#            {{ user_form.username.label }}:#}
{#            {{ user_form.username }}#}
{#            <div class="error" id="username-error"></div>#}
{#        </div>#}
{#        <div>#}
{#            {{ user_form.email.label }}:#}
{#            {{ user_form.email }}#}
{#            <div class="error" id="email-error"></div>#}
{#        </div>#}
{#        <div>#}
{#            {{ user_form.password1.label }}:#}
{#            {{ user_form.password1 }}#}
{#            <div class="error" id="password1-error"></div>#}
{#        </div>#}
{#        <div>#}
{#            {{ user_form.password2.label }}:#}
{#            {{ user_form.password2 }}#}
{#            <div class="error" id="password2-error"></div>#}
{#        </div>#}
{#        <div>#}
{#            <span>Я соглашаюсь с правилами регистрации:</span>#}
{#            {{ profile_form.rules }}#}
{#        </div>#}
{#        <button type="submit" name="CreateUser">Зарегистрироваться</button>#}
{#    </form>#}
{#    <div>Уже есть аккаунт? <a href="{% url 'login' %}">Войти</a></div>#}
{#    <script>#}
{#        document.addEventListener('DOMContentLoaded', function() {#}
{#            document.getElementById('registration-form').addEventListener('submit', function(event) {#}
{#                event.preventDefault(); // Отменяем стандартное поведение формы#}
{##}
{#                // Сбрасываем предыдущие ошибки#}
{#                document.querySelectorAll('.error').forEach(el => el.textContent = '');#}
{##}
{#                let isValid = true;#}
{##}
{#                const namePattern = /^[а-яА-ЯёЁ\s\-]+$/; // Для кириллицы (имя, фамилия, отчество)#}
{#                const usernamePattern = /^[a-zA-Z0-9\s\-]+$/; // Для латиницы (логин)#}
{##}
{#                const firstName = document.getElementById('id_first_name').value.trim();#}
{#                const lastName = document.getElementById('id_last_name').value.trim();#}
{#                const patronymic = document.getElementById('id_patronymic').value.trim();#}
{#                const username = document.getElementById('id_username').value.trim();#}
{##}
{#                // Проверка имени#}
{#                if (!namePattern.test(firstName)) {#}
{#                    document.getElementById('first-name-error').textContent = 'Имя может содержать только кириллицу, пробелы и тире.';#}
{#                    isValid = false;#}
{#                }#}
{##}
{#                // Проверка фамилии#}
{#                if (!namePattern.test(lastName)) {#}
{#                    document.getElementById('last-name-error').textContent = 'Фамилия может содержать только кириллицу, пробелы и тире.';#}
{#                    isValid = false;#}
{#                }#}
{##}
{#                // Проверка отчества#}
{#                if (patronymic && !namePattern.test(patronymic)) {#}
{#                    document.getElementById('patronymic-error').textContent = 'Отчество может содержать только кириллицу, пробелы и тире.';#}
{#                    isValid = false;#}
{#                }#}
{##}
{#                // Проверка логина#}
{#                if (!usernamePattern.test(username)) {#}
{#                    document.getElementById('username-error').textContent = 'Логин может содержать только латиницу, цифры, пробелы и тире.';#}
{#                    isValid = false;#}
{#                }#}
{##}
{#                // Если все проверки пройдены, отправляем форму#}
{#                if (isValid) {#}
{#                    this.submit(); // Отправляем форму, если данные валидны#}
{#                }#}
{#            });#}
{#        });#}
{#    </script>#}
{#</body>#}
{#</html>