<html>
    <head>
        <title>PHP Garbage</title>
    </head>

    <body>
        <h1>Times</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/');
            $obj = json_decode($json);
	          $laptops = $obj->Laptops;
            foreach ($laptops as $l) {
                echo "<li>$l</li>";
            }
            ?>
        </ul>
    </body>
</html>