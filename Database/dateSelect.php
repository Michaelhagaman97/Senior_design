<!DOCTYPE html>
<html>
<head>
<script src="updateTable.js"></script>
</head>
<body>

<?php

//TODO: set date by input variable
$date = htmlspecialchars($_GET['date']);
$upper = htmlspecialchars($_GET['upper']);

$con = mysqli_connect('localhost','root');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

//TODO: set date by input variable
mysqli_select_db($con,"test");

if($upper != null){
	$sql="SELECT * FROM testdatetime WHERE picDate BETWEEN '" . $date . "' AND '" . $upper . "' ORDER BY picDate";
}
else if($date == null){
	return false;
}
else{
	$sql="SELECT * FROM testdatetime WHERE picDate='" . $date . "'";
}

$result = mysqli_query($con,$sql);

echo "<table id=\"selection\">
<tr>
<th>Go to:</th>
<th>Date</th>
<th>Time</th>
<th>Hog Present?</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
	$x = "getImage('" . $row['picLoc'] . "')";
	echo "<tr>";
	echo "<td>" . "<button class=\"button\" onclick=\"" . $x . "\">Go</button>". "</td>";
	echo "<td>" . $row['picDate'] . "</td>";
	echo "<td>" . $row['picTime'] . "</td>";
	echo "<td>" . $row['hogPresent'] . "</td>";
	echo "</tr>";
}

echo "</table>";

mysqli_close($con);

?>
</body>
</html> 