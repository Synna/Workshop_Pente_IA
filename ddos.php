<?php
while (true) {
	$url="https://pente-server.herokuapp.com/connect/coucou"; 

	$options=array(
	      CURLOPT_URL            => $url,
	      CURLOPT_RETURNTRANSFER => true,
	      CURLOPT_HEADER         => false
	);
	 
	$CURL=curl_init();
	 
	      curl_setopt_array($CURL,$options);
	 
	      $content=curl_exec($CURL);
	curl_close($CURL);
	echo $content;
}