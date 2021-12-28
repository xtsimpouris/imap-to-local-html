<ul class="nav flex-column">
    <li class="nav-item">
        {% for menu in menuToShow %}
            {% if menu.selected %}
                {% if menu.id == selectedFolder or menu.id in selectedFolder %}
                    <a class="nav-link active" href="{{linkPrefix}}{{ menu.link }}" data-id="{{ menu.id }}">
                        {{ menu.title }}
                    </a>
                {% else %}
                    <a class="nav-link" href="{{linkPrefix}}{{ menu.link }}" data-id="{{ menu.id }}">
                        {{ menu.title }}
                    </a>
                {% endif %}
            {% else %}
                <a class="nav-link not-selected" href="{{linkPrefix}}{{ menu.link }}" data-id="{{ menu.id }}">
                    {{ menu.title }}
                </a>
            {% endif %}
            {% if menu.children %}
                {{ menu.children }}
            {% endif %}
        {% endfor %}
    </li>
</ul>
