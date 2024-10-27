<!DOCTYPE html>#}
{#<html lang="en">#}
{#<head>#}
{#    <meta charset="UTF-8">#}
{#    <meta name="viewport" content="width=device-width, initial-scale=1.0">#}
{#    <title>Личный кабинет</title>#}
{#</head>#}
{#<body>#}
{#    <h1>Ваши брони</h1>#}
{##}
{#    {% if reservations %}#}
{#        <table>#}
{#            <thead>#}
{#                <tr>#}
{#                    <th>Продукт</th>#}
{#                    <th>Количество</th>#}
{#                    <th>Дата</th>#}
{#                </tr>#}
{#            </thead>#}
{#            <tbody>#}
{#                {% for reservation in reservations %}#}
{#                <tr>#}
{#                    <td>{{ reservation.product.name }}</td>#}
{#                    <td>{{ reservation.quantity }}</td>#}
{#                    <td>{{ reservation.date }}</td>#}
{#                </tr>#}
{#                {% endfor %}#}
{#            </tbody>#}
{#        </table>#}
{#    {% else %}#}
{#        <p>У вас нет броней.</p>#}
{#    {% endif %}#}
{#    #}
{#    <a href="{% url 'reserve_food' %}">Забронировать еду</a>#}
{#</body>#}
{#</html>