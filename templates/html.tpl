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
    <link rel="stylesheet" href="{{linkPrefix}}/inc/datatables/jquery.dataTables.min.css">

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
    <script src="{{linkPrefix}}/inc/js/jquery-3.6.0.min.js"></script>
    <script src="{{linkPrefix}}/inc/js/popper.min.js"></script>
    <script src="{{linkPrefix}}/inc/js/bootstrap.min.js"></script>
    <script src="{{linkPrefix}}/inc/datatables/jquery.dataTables.min.js"></script>
    <script type="text/javascript">
      $(document).ready( function () {
        $('.datatable').DataTable();
      });
    </script>
  </body>
</html>
