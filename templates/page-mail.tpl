{% for folderID in mail.folders %}
  <div class="col-sm-12 text-right no-padding">
    {{ folderID|renderFolderBreadcrump(linkPrefix) }}
  </div>
{% endfor %}

<ul class="list-group">
  <li class="list-group-item">
    <div class="row">
      <div class="col-md-3 text-right">
        <strong>From:</strong>
      </div>
      <div class="col-md-9">
        {{ mail.from|e }}
      </div>
    </div>
  </li>
  <li class="list-group-item">
    <div class="row">
      <div class="col-md-3 text-right">
        <strong>To:</strong>
      </div>
      <div class="col-md-9">
        {{ mail.to|e }}
      </div>
    </div>
  </li>
  <li class="list-group-item">
    <div class="row">
      <div class="col-md-3 text-right">
        <strong>Subject:</strong>
      </div>
      <div class="col-md-9">
        {{ mail.subject|e }}
      </div>
    </div>
  </li>
  <li class="list-group-item">
    <div class="row">
      <div class="col-md-3 text-right">
        <strong>Date:</strong>
      </div>
      <div class="col-md-9">
        {{ mail.date }}
      </div>
    </div>
  </li>
  {% if mail.replyTo and mail.replyTo.link %}
    <li class="list-group-item">
      <div class="row">
        <div class="col-md-3 text-right">
          <strong>Reply to:</strong>
        </div>
        <div class="col-md-9">
          <a href="{{ linkPrefix }}{{ mail.replyTo.link }}">{{ mail.replyTo.subject }}</a>
        </div>
      </div>
    </li>
  {% endif %}
  {% if thread %}
    <li class="list-group-item">
      <div class="row">
        <div class="col-md-3 text-right">
          <strong>Thread:</strong>
        </div>
        <div class="col-md-9">
          {{ thread|safe }}
        </div>
      </div>
    </li>
  {% endif %}
  <li class="list-group-item">
    <div class="row">
      <div class="col-md-3 text-right">
        <strong>Message ID:</strong>
      </div>
      <div class="col-md-9">
        {{ mail.id|e }}
      </div>
    </div>
  </li>
  {% if mail.attachments %}
    <li class="list-group-item">
      <div class="row">
        <div class="col-md-3 text-right">
          <strong>Attachment(s):</strong>
        </div>
        <div class="col-md-9">
          <ol class="attachments">
            {% for attachment in mail.attachments %}
              <li><a href="{{ linkPrefix }}/{{ attachment.link }}" target="_blank">{{ attachment.title }}</a> ({{ attachment.size|humansize }}, {{ attachment.mimetype }})</li>
            {% endfor %}
          </ol>
        </div>
      </div>
    </li>
  {% endif %}
  {% if mail.error_decoding %}
    <li class="list-group-item btn-outline-danger">
      <div class="row">
        <div class="col-md-3 text-right">
          <strong>Error decoding:</strong>
        </div>
        <div class="col-md-9">
          {{ mail.error_decoding|e }}
        </div>
      </div>
    </li>
  {% endif %}
</ul>
<div id="mail-content">
  <ul class="nav nav-tabs" id="mail-content-tab" role="tablist">
    {% if mail.content.html %}
      <li class="nav-item">
        <a class="nav-link {% if mail.content.default == 'html' %}active{% endif %}" data-toggle="tab" id="content-tab-html" href="#content-html" role="tab" aria-controls="content-html" aria-selected="false">HTML</a>
      </li>
    {% else %}
      <li class="nav-item">
        <a class="nav-link disabled" data-toggle="tab" id="content-tab-html" href="#content-html" role="tab" aria-controls="content-html" aria-selected="false">HTML</a>
      </li>
    {% endif %}
  
    {% if mail.content.text %}
      <li class="nav-item">
        <a class="nav-link {% if mail.content.default == 'text' %}active{% endif %}" data-toggle="tab" id="content-tab-text" href="#content-text" role="tab" aria-controls="content-text" aria-selected="false">Text</a>
      </li>
    {% else %}
      <li class="nav-item">
        <a class="nav-link disabled" data-toggle="tab" id="content-tab-text" href="#content-text" role="tab" aria-controls="content-text" aria-selected="false">Text</a>
      </li>
    {% endif %}
  
    {% if mail.content.raw %}
      <li class="nav-item">
        <a class="nav-link {% if mail.content.default == 'raw' %}active{% endif %}" data-toggle="tab" id="content-tab-raw" href="#content-raw" role="tab" aria-controls="content-raw" aria-selected="false">Raw</a>
      </li>
    {% else %}
      <li class="nav-item">
        <a class="nav-link disabled" data-toggle="tab" id="content-tab-raw" href="#content-raw" role="tab" aria-controls="content-raw" aria-selected="false">Raw</a>
      </li>
    {% endif %}
  </ul>
  <div class="tab-content">
    <div class="tab-pane fade {% if mail.content.default == 'html' %}show active{% endif %}" id="content-html" role="tabpanel" aria-labelledby="content-tab-html">
      {{ mail.content.html|safe }}
    </div>
    <div class="tab-pane fade {% if mail.content.default == 'text' %}show active{% endif %}" id="content-text" role="tabpanel" aria-labelledby="content-tab-text">
      <pre>{{ mail.content.text|safe }}</pre>
    </div>
    <div class="tab-pane fade {% if mail.content.default == 'raw' %}show active{% endif %}" id="content-raw" role="tabpanel" aria-labelledby="content-tab-raw">
      {% if mail.download %}
        <div class="float-right"><a href="{{ mail.download.content }}" download="{{ mail.download.filename }}">Download as EML file</a></div>
      {% endif %}
      <pre>{{ mail.content.raw|e }}</pre>
    </div>
  </div>
</div>
