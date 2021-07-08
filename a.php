<html>
 <body>
  <head>
   <title>
     run
   </title>
  </head>

   <form method="get">

    <input type="submit" value="GO" name="GO">
   </form>
 </body>
</html>

<?php
	if(isset($_GET['GO']))
	{
		shell_exec("python owr7/github.io/new2.py");
		echo"success";
	}
?>
