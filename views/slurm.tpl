<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="css/main.css" />

 	<link rel="shortcut icon" href="img/favicon.ico" />

 	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<!-- ######################################################################################################### -->
	<!-- SCRIPTS START -->	

 	<!-- jquery must come first and is required by bootstrap -->
	<script src="js/jquery-3.1.0.min.js"></script>
	<script src="js/bootstrap.min.js"></script>

	<!-- custom js functions -->
	% include('_js_functions.tpl')

	<!-- SCRIPTS END -->
	<!-- ######################################################################################################### -->

</head>


<!-- PASSED IN FROM ROUTE -->
<!-- time : current time -->
<!-- outputs : [str] from all the states -->

<body>

<!-- main container start -->
<div class="container" name="main">

<!-- outputs row start -->
% include('_outputs.tpl', anchorHere=anchor, requested=requested, scontrol_result=scontrol_result)
<!-- outputs row end -->

</div>
<!-- main container end -->

</body>

</html>