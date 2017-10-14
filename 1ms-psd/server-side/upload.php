<?php

if($_POST["pw"] != "PDP11")
{
	die("Password needed for the upload.");
}

//TODO: prevent php injection

$move_path = "./" . basename($_FILES["fileformID"]["name"]);


if(move_uploaded_file($_FILES["fileformID"]["tmp_name"],$move_path))
{
	echo "1";
}
else
{
	echo "0";
}


?>
