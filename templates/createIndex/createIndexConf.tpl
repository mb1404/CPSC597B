<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Python SQLite Admin Tool</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />

    <!-- Le styles -->
    <link href="../../../static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <script src="../../../static/bootstrap/js/jquery-1.10.2.min.js"></script>

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
    <link href="../../../static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">

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
        
        function chk_if_col_checked(){
            
            x = document.getElementsByName("col");
            ischecked = false;
            
            for (var i=0;i<x.length;i++)
            { 
                if(document.getElementsByName("col")[i].checked == true){
                    ischecked = true;
                }
            }
           
           if(ischecked)
           {
              document.getElementsByName("create_index_btn")[0].disabled = false; 
           }
           else{
               document.getElementsByName("create_index_btn")[0].disabled = true; 
           }
        }
        
       /* $(document).ready(function(){
          $("#displayDIV").click(function(){
            $("#addColDIV").show();
          });
        });*/

        
        //this function will validate the form
        /*function validateForm(){
            var cn=document.forms["addColForm"]["ColName"].value;
            if (cn==null || cn==""){
              alert("Column name must be filled out");
                return false;
            }
        }*/
        
        
        
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
                    %if name == choosenDB:
                        <option value="/database/{{name}}" selected>{{name}}</option>
                    %else:
                        <option value="/database/{{name}}">{{name}}</option>
                    %end
                  %end
                  
                </select>
              </li>
              <li><a href="/createdb">Create New Database</a></li>
              <li><a href="/dropdb">Drop Database</a></li>
              <li><a href="/uploadDB">Upload Database</a></li>
              <li><a href="/SQLiteDatabases/{{choosenDB}}">Download Database</a></li>
            </ul>
          </div><!--/.well -->
          
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Tables</li>
              <li><a href="/database/{{choosenDB}}/createTable">Create Table</a></li>
              <li><a href="/database/{{choosenDB}}/dropTable">Drop Table</a></li>
              <li><a href="/database/{{choosenDB}}/manageTable/frontPage">Manage Table</a></li>
              
              <li class="nav-header">Index</li>
              <li class="active"><a href="/database/{{choosenDB}}/createIndex">Create Index</a></li>
              <li><a href="/database/{{choosenDB}}/dropIndex">Drop Index</a></li

              <li class="nav-header">Views</li>
              <li><a href="/database/{{choosenDB}}/createView">Create View</a></li>
              <li><a href="/database/{{choosenDB}}/manageView">Manage View</a></li>
              
              <li class="nav-header">Data</li>
              <li><a href="manageData/frontPage">Manage Data</a></li>
              <li><a href="/database/{{choosenDB}}/SQLQuery">SQL query</a></li>
              <li><a href="/database/{{choosenDB}}/exportData">Export Data</a></li>
              <li><a href="/database/{{choosenDB}}/importData">Import Data</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        
        
        <div class="span9">
          <div class="hero-unit" style="background:#eeeeee;padding: 10px;">
            <center><h2>Create Index</h2></center>
            </div>
          <div class="row-fluid">
            <div class="span12">
                <form action="/database/{{choosenDB}}/createIndex/{{tableName}}" method="POST" name="createIndexForm" class="form-inline">
                    
                    <table cellpadding="15">
                        <fieldset>
                        
                        <tr>
                            <td>
                                <label>Table</label>
                            </td>
                            <td>
                                <select onchange="this.options[this.selectedIndex].value && (window.location = '/database/{{choosenDB}}/createIndex/' + this.options[this.selectedIndex].value);" class="input-medium" name="tableN">
                                  %for tableN in tablesList:
                                      %if tableN == tableName:
                                        <option value="{{tableN}}" selected>{{tableN}}</option>
                                      %else:
                                        <option value="{{tableN}}">{{tableN}}</option>
                                      %end
                                  %end
                                </select>
                            </td>
                        </tr>
                        
                        
                        <tr>
                            <td>
                                <label>Index Name</label>
                            </td>
                            <td>
                                <input type="text" class="input-medium" name="IndexName">
                            </td>
                        </tr>
                        
                        <tr>
                            <td>
                                <label>Choose Columns</label><br>
                                %for colN in tableColNames:
                                    &nbsp;&nbsp;&nbsp;<input type="checkbox" name="col" value="{{colN}}" onclick="chk_if_col_checked()"> {{colN}} <br>
                                %end
                            <td>
                        </tr>
                        
                        
                        <tr>
                            <td>
                                <button type="submit" class="btn" name = "create_index_btn" value="create" disabled>Create Index</button>
                            </td>
                        </tr>
                        </fieldset>
                    
                    </table>

               
               
                </form>  
                
                <p>
                    %if "succesfully" in message:
                        <span style="color:green;">{{message}}</span>
                    %else:
                        <span style="color:red;">{{message}}</span>
                    %end
                    
                </p>
                
            </div><!--/span-->
          </div><!--/row-->
          
        </div><!--/span-->
      </div><!--/row-->

      <hr>

      

    </div><!--/.fluid-container-->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../../../static/bootstrap/js/jquery.js"></script>
    <script src="../../../static/bootstrap/js/bootstrap.js"></script>
    <script src="../../../static/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
