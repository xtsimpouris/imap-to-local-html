<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="{{linkPrefix}}/inc/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{linkPrefix}}/inc/bootstrap-icons/bootstrap-icons.css">
    <link rel="stylesheet" href="{{linkPrefix}}/inc/css/dashboard.css">

    <title>{{ title }}</title>
    <meta name="generator" content="IMAP to local HTML, https://github.com/xtsimpouris/imap-to-local-html">
  </head>
  <body>
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
        <a class="navbar-brand col-sm-6 col-md-4 mr-0" href="{{linkPrefix}}/index.html">{{ username }}</a>
    </nav>
    <div class="row">
        <nav class="col-md-4 d-none d-md-block col-lg-2 bg-light sidebar">
          <div class="sidebar-sticky">
            {{ sideMenu }}
          </div>
        </nav>
    
        <main role="main" class="col-md-8 ml-sm-auto col-lg-10 px-4">
          <div id="content">
            {{ header }}
            {{ content }}
          </div>
        </main>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="{{linkPrefix}}/inc/js/bootstrap.min.js"></script>
  </body>
</html>
