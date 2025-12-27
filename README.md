Notes :

-  Disable  insecure Content from site settings next to site in address bar  --- > from block to allow in order to resolve the issue of mixed content issue
   because S3 bcuket is HTTPS and api backend is http .. 
-  the main issue was CORS ERROR shown in browsers
-  CORS meaning :  Browser will allow Java script to reply to same origin which load index.html with java  other wise browser will block it
-  to resolve  destination like pyhon flask should configured o allow CORS  --> 'hey broswer I am allow this jave to send the request to me "
-  index will be in s3 bucket


