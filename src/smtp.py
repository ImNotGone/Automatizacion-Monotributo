import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(client, receiver_email, email_credentials):
    smtp_server = email_credentials["smtp_server"]
    smtp_port = email_credentials["smtp_port"]
    smtp_username = email_credentials["smtp_username"]
    smtp_password = email_credentials["smtp_password"]

    # armo el cuerpo del email
    msg = MIMEMultipart()
    sender_email = smtp_username
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"ALERT! {client} has balance < 0"
    message = f"This email was sent because {client} has a negative balance!!"
    msg.attach(MIMEText(message, 'plain'))

    # intento enviar el email
    server = None
    try:
        # abro la conecxion y me autorizo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # envio el email
        server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print('Error:', e)
    finally:
        if server:
            # si se inicio cierro la conecxion
            server.quit()
