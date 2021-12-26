<label>Here is the information you gave me:</label>
{% for info in allInfo %}
    <div class="input-group mb-3">
        <div class="input-group-prepend">
            <span class="input-group-text" id="{{ info.title }}-span">{{ info.title }}</span>
        </div>
        <input type="text" class="form-control" id="{{ info.title }}" aria-describedby="{{ info.title }}-span" value="{{ info.value }}" disabled />
    </div>
{% endfor %}
