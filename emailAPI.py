def sendMail(email,password):
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	
	me = "prakashrakeshiya669@gmail.com"
	you = email

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Verification Mail eAuction"
	msg['From'] = me
	msg['To'] = you

	html = """<html>
  					<head></head>
  					<body>
    					<h1>Welcome to eAuction</h1>
    					<p>You have successfully registered your login credentials are attached below , please click on the link below to verify your account</p>
    					<h2>Username : """+email+"""</h2>
    					<h2>Password : """+str(password)+"""</h2>
    					<br>
    					<a href='http://localhost:8000/verify?vemail="""+email+"""' >Click here to verify account</a>		
  					</body>
				</html>
			"""
	
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login("prakashrakeshiya669@gmail.com", "xrcfqbwnympadhtq") 
	
	part2 = MIMEText(html, 'html')

	msg.attach(part2)
	
	s.sendmail(me,you, str(msg)) 
	s.quit() 
	print("mail send successfully....")
