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
    <link href="../../static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <script src="../../static/bootstrap/js/jquery-1.10.2.min.js"></script>

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
    <link href="../../static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">

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
        
        
        //this function will validate the form
        function validateForm(){
            var tn=document.forms["createTableForm"]["tableName"].value;
            if (tn==null || tn==""){
              alert("Table Name must be filled out");
                return false;
            }
            
            var cn=document.forms["createTableForm"]["ColName1"].value;
            if (cn==null || cn==""){
              alert("Column name must be filled out");
                return false;
            }
        }
        
        
        //This function will insert a new row to the table
        function insertRow(){
            var table=document.getElementById("ctTable");
            var rowsNum = table.rows.length;
            
            columnName = '<td><input type="text" class="input-medium" name="ColName'+rowsNum+'"></td>';
            
            columonType = '<td><select name="colType'+rowsNum+'" class="input-medium" > ' +
                              '<option>INTEGER</option> ' +
                              '<option>REAL</option> ' + 
                              '<option>TEXT</option> ' + 
                              '<option>NUMERIC</option>' + 
                              '<option>NONE</option> ' +                   
                              '</select>' +
                          '</td>';
            
            isNull = '<td>' +
                          '<select name="isNull'+rowsNum+'" class="input-small" >' +
                              '<option value="False">Null</option>' +
                              '<option value="True">Not Null</option>' +
                          '</select>' +
                     '</td>';
            
            autoI = '<td>' + 
                          '<select name="isAI'+rowsNum+'" class="input-small" >' + 
                              '<option value="True">Yes</option>' + 
                              '<option value="False" selected>No</option>' + 
                          '</select>' + 
                    '</td>';
            
            defaultF = '<td><input type="text" class="input-small" name="defaultValue'+rowsNum+'"></td>';
            
            isPK = '<td>' +
                          '<select name="isPK'+rowsNum+'" class="input-small" >' +
                              '<option value="True">Yes</option>' +
                              '<option value="False"selected >No</option>' +
                         '</select>' +
                   '</td>';
            
            var row=table.insertRow(-1);
            row.innerHTML= columnName + columonType + isNull + autoI + defaultF + isPK;

        }
        
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
              <li class="active"><a href="/database/{{choosenDB}}/createTable">Create Table</a></li>
              <li><a href="/database/{{choosenDB}}/dropTable">Drop Table</a></li>
               <li><a href="/database/{{choosenDB}}/manageTable/frontPage">Manage Table</a></li>
               
               <li class="nav-header">Index</li>
              <li><a href="/database/{{choosenDB}}/createIndex">Create Index</a></li>
              <li><a href="/database/{{choosenDB}}/dropIndex">Drop Index</a></li>

              <li class="nav-header">Views</li>
              <li><a href="/database/{{choosenDB}}/createView">Create View</a></li>
              <li><a href="/database/{{choosenDB}}/manageView">Manage View</a></li>
              
              <li class="nav-header">Data</li>
                <li><a href="/database/{{choosenDB}}/manageData/frontPage">Manage Data</a></li>
              <li><a href="/database/{{choosenDB}}/SQLQuery">SQL query</a></li>
              <li><a href="/database/{{choosenDB}}/exportData">Export Data</a></li>
              <li><a href="/database/{{choosenDB}}/importData">Import Data</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        
        
        <div class="span9">
          <div class="hero-unit" style="background:#eeeeee;padding: 10px;">
            <center><h2>Create Table</h2></center>
            </div>
          <div class="row-fluid">
            <div class="span12">
              
                <form name="createTableForm" class="form-inline" onsubmit="return validateForm()">
                   New Table Name:
                  <input type="text" class="input-medium" name="tableName">
                  <br><br>
                  
                  <table id="ctTable" class="table">
                  <thead>
                    <tr>
                      <th>Column Name</th>
                      <th>Column Type</th>
                      <th>Is Null</th>
                      <th>Auto Increment</th>
                      <th>Default Value</th>
                      <th>is pk</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                        
                      <td><input type="text" class="input-medium" name="ColName1"></td>
                      
                      <td><select name="colType1" class="input-medium" >
                          <option>INTEGER</option>
                          <option>REAL</option>
                          <option>TEXT</option>
                          <option>NUMERIC</option> 
                          <option>NONE</option>                         
                        </select>
                      </td>
                      
                      
                      <td>
                          <select name="isNull1" class="input-small" >
                              <option value="False">Null</option>
                              <option value="True">Not Null</option>
                        </select>
                      </td>
                      
                      
                      <td>
                          <select name="isAI1" class="input-small" >
                              <option value="True">Yes</option>
                              <option value="False" selected>No</option>
                          </select>
                      </td>
                      
                      <td><input type="text" class="input-small" name="defaultValue1"></td>
                      
                      
                      <td>
                          <select name="isPK1" class="input-small" >
                              <option value="True">Yes</option>
                              <option value="False"selected >No</option>
                          </select>
                      </td>
                      
                    </tr>
                  </tbody>
                </table>
                  <button type="button" class="btn" onclick="insertRow()">Insert new row</button>
                  
                <br><br>
                  <button type="submit" class="btn" name = "create_table_btn" value="create">Create</button>
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
    <script src="../../static/bootstrap/js/jquery.js"></script>
    <script src="../../static/bootstrap/js/bootstrap.js"></script>
    <script src="../../static/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
