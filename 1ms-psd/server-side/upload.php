<?php

//A Simple PHP server-side script for automatic upload of collected data.

//Credentials Check
if($_POST["pw"] != "PDP11")	//PW
{
	die("Password needed for the upload.");
}

//TODO: prevent php injection
//Path to store
$move_path = "./" . basename($_FILES["fileformID"]["name"]);

//Move from temp location to the permanant path
if(move_uploaded_file($_FILES["fileformID"]["tmp_name"],$move_path))
{
	echo "1";	//success
}
else
{
	echo "0";	//fail
}

?>
