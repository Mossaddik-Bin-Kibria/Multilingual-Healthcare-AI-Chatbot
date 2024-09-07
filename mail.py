import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body, to_email):
    # Email configuration
    from_email = "testingsubject2024@gmail.com"
    email_password = "aggc yivq eesr ilum"
    
    # Create the email header
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server (or another SMTP server)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(from_email, email_password)  # Log in to the email account
        text = msg.as_string()
        
        # Send the email
        server.sendmail(from_email, to_email, text)
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        # Close the server connection
        server.quit()

# Example usage
send_email_alert(
    subject="Security Alert",
    body="Your data was accessed without authorization!",
    to_email="example@gmail.com"
)
