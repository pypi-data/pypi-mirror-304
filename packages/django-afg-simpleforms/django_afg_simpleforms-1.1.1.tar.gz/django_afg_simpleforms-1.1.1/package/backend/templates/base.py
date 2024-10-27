<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ category.name }}</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'css/images.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'css/h1.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'css/button.css' %}">
    <style>
        body{
            background-image: url("{% static 'images/фон.svg' %}");
            background-size: 100%;
        }
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
</head>
<body>
{% include "base/menu.html" %}
{% block content %}
{% for item in paginated_categories %}
<h2 style="margin-left: 2.5vw;">{{ item.category.name }}</h2>
{% if item.media_page|length > 0 %}
<div class="image-container">
    {% for media in item.media_page %}
    <div class="image-item"
         onclick="openModal('{{ media.image.url }}', '{{ media.name }}', '{{ media.description }}', '{{ media.media_id }}', {{ media.get_unique_views_count }})">
        <h3>{{ media.name }}</h3>
        <img src="{{ media.image.url }}" alt="{{ media.name }}">
        <p>Просмотров: {{ media.get_unique_views_count }}</p>
    </div>
    {% endfor %}
</div>

<!-- Pagination -->
<div class="pagination">
    <span class="step-links">
        {% for page_num in item.media_page.paginator.page_range %}
            {% if page_num == item.media_page.number %}
        <button class="buttone">{{ page_num }}</button>
            {% else %}
                <a href="?page={{ page_num }}"><button>{{ page_num }}</button></a>
            {% endif %}
        {% endfor %}

        {% if item.media_page.has_previous %}
            <a href="?page=1"><button>First</button></a>
            <a href="?page={{ item.media_page.previous_page_number }}"><button>Previous</button></a>
        {% endif %}

        {% if item.media_page.has_next %}
            <a href="?page={{ item.media_page.next_page_number }}"><button>Next</button></a>
            <a href="?page={{ item.media_page.paginator.num_pages }}"><button>Last</button></a>
        {% endif %}

        <span class="current">
            Page {{ item.media_page.number }} of {{ item.media_page.paginator.num_pages }}.
        </span>
    </span>
</div>

{% else %}
<p style="margin-left: 2.5vw;">No images available.</p>
{% endif %}
{% endfor %}
{% endblock %}
<!-- The Modal -->
<div id="myModal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeModal()">&times;</span>
        <div class="carousel">
            <span class="prev" onclick="prevSlide('{{ media.media_id }}')">&#10094;</span>
            <div class="carousel-images">
                <img id="modalImage" src="" alt="">
                <div id="modalDescription"></div>
                <div id="modalViews"></div>
            </div>
            <span class="next" onclick="nextSlide('{{ media.media_id }}')">&#10095;</span>
        </div>
    </div>
</div>

<script>
    let modal = document.getElementById('myModal');
    let modalImage = document.getElementById('modalImage');
    let modalDescription = document.getElementById('modalDescription');
    let modalViews = document.getElementById('modalViews');
    let images = [];
    let currentIndex = 0;

    let currentMediaId;

    function openModal(imageSrc, name, description, id, views) {
        $.ajax({
            type: 'GET',
            url: '/update_views/',
            data: {
                media_id: id,
            },
            success: function(data) {
                console.log(data);
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log('Error:', errorThrown);
            }
        });

        modal.style.display = 'block';
        modalImage.src = imageSrc;
        modalDescription.innerHTML = '<h3>' + name + '</h3><p>' + description + '</p>';
        currentMediaId = id;

        images = Array.from(document.querySelectorAll('.image-item img')).map(img => {
            return {
                url: img.src,
                name: img.alt,
                description: img.parentElement.querySelector('p').innerText
            };
        });

        currentIndex = images.findIndex(img => img.url === imageSrc);

         document.querySelector('.prev').onclick = () => prevSlide(id);
         document.querySelector('.next').onclick = () => nextSlide(id);

    }

    function closeModal() {
        modal.style.display = 'none';
    }

    function prevSlide(id) {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : images.length - 1;
    updateModalImage();
    $.ajax({
        type: 'GET',
        url: '/update_views/',
        data: {
            media_id: currentMediaId,
        },
        success: function(data) {
            console.log(data);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log('Error:', errorThrown);
        }
    });
}

    function nextSlide(id) {
        currentIndex = (currentIndex < images.length - 1) ? currentIndex + 1 : 0;
        updateModalImage();
        $.ajax({
            type: 'GET',
            url: '/update_views/',

            data: {

                media_id: currentMediaId,

            },

            success: function(data) {

                console.log(data);

            },

            error: function(xhr, textStatus, errorThrown) {

                console.log('Error:', errorThrown);

            }

        });

    }



    function updateModalImage() {

        modalImage.src = images[currentIndex].url;

        modalDescription.innerHTML = '<h3>' + images[currentIndex].name + '</h3><p>' + images[currentIndex].description + '</p>';

    }

    document.onkeydown = function(e) {
        if (modal.style.display === 'block') {
            if (e.key === 'ArrowLeft') {
                prevSlide(currentMediaId);
            } else if (e.key === 'ArrowRight') {
                nextSlide(currentMediaId);
            } else if (e.key === 'Escape')
                closeModal();


    };
</script>
</body>
</html>