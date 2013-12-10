<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Python SQLite Admin Tool</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <script src="static/bootstrap/js/jquery-1.10.2.min.js"></script>

    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      .sidebar-nav {
        padding: 9px 0;
      }

      @media (max-width: 980px) {
        /* Enable use of floated navbar text */
        .navbar-text.pull-right {
          float: none;
          padding-left: 5px;
          padding-right: 5px;
        }
      }
    </style>
    <link href="static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">

     <script>
        //the following javascrip function is used to redirect to the database page after a database is chosen
        $(function(){
          $('#dynamic_select').bind('change', function () {
              var url = $(this).val();
              if (url) {
                  window.location = url;
              }
              return false;
          });
        });
    </script>
    
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="brand" href="#">Python SQLite Admin Tool</a>
        </div>
      </div>
    </div>

    <!--left menu-->
    <div class="container-fluid">
      <div class="row-fluid">
        <div class="span3">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Choose Database</li>
              <li><select id="dynamic_select">
                  <option></option>
                  %for name in dbNames:
                       <option value="/database/{{name}}">{{name}}</option>
                  %end
                </select>
                </li>
                <li><a href="/createdb">Create New Database</a></li>
                <li class="active"><a href="/dropdb">Drop Database</a></li>
                <li><a href="/uploadDB">Upload Database</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        
        
        <div class="span9">
          <div class="hero-unit" style="background:#eeeeee;padding: 10px;">
            <center><h2>Drop Database</h2></center>
            </div>
          <div class="row-fluid">
            <div class="span12">
              
             
                  <form class="form-inline">
                   Database Name:
                  <select name="databaseName">
                  %for name in dbNames:
                    <option>{{name}}</option>
                  %end
                </select>
                  <br><br>
                  <button type="submit" class="btn" name = "drop_db_btn" value="drop">Drop</button>
                </form>
                  
              
            </div><!--/span-->
          </div><!--/row-->
        </div><!--/span-->
      </div><!--/row-->

      <hr>

      

    </div><!--/.fluid-container-->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="static/bootstrap/js/jquery.js"></script>
    <script src="static/bootstrap/js/bootstrap.js"></script>
    <script src="static/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
