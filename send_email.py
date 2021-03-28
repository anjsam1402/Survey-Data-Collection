from email.mime.text import MIMEText
import smtplib

def send(email, height, average, count):
   from_email = "samad.anjali.1402@gmail.com"
   from_password = "@nj@li14@"
   to_email = email

   subject = "Height Data Survey"
   message = "Hey there, Your height is <strong>%s</strong>. Average height is <strong>%s</strong> \
   counted from total of <strong>%s</strong> users. Thanks for your participation !!!!" % (height, average, count)

   msg = MIMEText(message, 'html')
   msg['Subject'] = subject
   msg['To'] = to_email
   msg['From'] = from_email

   gmail = smtplib.SMTP('smtp.gmail.com', 587)
   gmail.ehlo()
   gmail.starttls()
   gmail.ehlo()
   gmail.login(from_email, from_password)
   gmail.send_message(msg)

