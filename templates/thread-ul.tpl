<ul>
    {% for mail in mailToShow %}
        <li>
            {% if mail.link %}
                {% if mail.selected %}
                    <a href="{{linkPrefix}}{{ mail.link }}" data-id="{{ mail.id }}">
                        <strong>{{ mail.subject }}</strong>
                    </a>
                    ({{ mail.date|strftime }})
                {% else %}
                    <a href="{{linkPrefix}}{{ mail.link }}" data-id="{{ mail.id }}">
                        {{ mail.subject }}
                    </a>
                    ({{ mail.date|strftime }})
                {% endif %}
            {% else %}
                <span data-id="{{ mail.id }}">
                    {{ mail.subject }}
                    ({{ mail.date|strftime }})
                </span>
            {% endif %}
            {% if mail.children %}
                {{ mail.children }}
            {% endif %}
        </li>
    {% endfor %}
</ul>
