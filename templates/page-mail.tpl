<ul class="list-group">
    <li class="list-group-item"><strong>From:</strong> {{ mail.from }}</li>
    <li class="list-group-item"><strong>To:</strong> {{ mail.to }}</li>
    <li class="list-group-item"><strong>Subject:</strong> {{ mail.subject }}</li>
    <li class="list-group-item"><strong>Date:</strong> {{ mail.date }}</li>
    <li class="list-group-item"><strong>Raw:</strong> Click here to download raw file as eml</li>
</ul>
{{ mail.id }}
