# import os
# from flask import Flask, request
# from celery import Celery
# from email.mime.text import MIMEText
# import logging
# from datetime import datetime
# import smtplib

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize Celery with RabbitMQ broker
# celery = Celery(app.import_name, broker='amqp://localhost:5672')

# # Setup logging
# logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

# # Celery task definition
# @celery.task(name='send_email_task')
# def send_email_task(recipient='jacinth.david@stu.cu.edu.ng'):
#     # Load email credentials from environment variables (recommended)
#     sender = os.environ.get('siickart69@gmail.com')
#     password = os.environ.get('Endocrine70')

#     # OR use an app password generated from Google account settings (more secure)

#     subject = "Test Email"
#     body = f"This is a test email sent from your local machine at {datetime.now()}"
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = sender
#     msg['To'] = recipient

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
#         smtp_server.login(sender, password)
#         smtp_server.sendmail(sender, recipient, msg.as_string())

#     logging.info(f"Email sent to {recipient}")

# # Endpoint for handling requests
# @app.route('/')
# def handle_requests():
#     if 'sendmail' in request.args:
#         recipient = request.args.get('sendmail')
#         send_email_task.delay(recipient)
#         return f"Email task queued for sending to {recipient}\n"
#     elif 'talktome' in request.args:
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         logging.info(f"Talktome request recieved at {current_time}")
#         return f"Current time logged: {current_time}"
#     else:
#         return "Invalid request. Use ?sendmail or ?talktome parameter."

# # Run the Flask application
# if __name__ == '__main__':
#     app.run(debug=True)




import os
# from flask import Flask, request
from email.mime.text import MIMEText
import logging
from datetime import datetime
import smtplib
from celery import Celery
from flask_mail import Mail, Message
from flask import Flask
import time

# Initialize Flask app
app = Flask(__name__)

# Flask-Mail configuration for Gmail 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Gmail SMTP SSL port
app.config['MAIL_USE_SSL'] = True  # Enable SSL encryption
app.config['MAIL_USERNAME'] = 'siickart69@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'Endocrine70'  # Replace with your app password

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://localhost:5672//'  # Replace with your broker URL
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'  # Replace with your preferred result backend

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    celery.autodiscover_tasks(['app'])  # Ensure the app module is discovered
    return celery

celery = make_celery(app)

# Celery task: send_email
@celery.task(name='app.send_email')  # Register the task with a specific name
def send_email(to):
    msg = Message("Test Email", sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = "This is a test email."

    try:
        with app.app_context():
            mail.send(msg)
        print(f"Sent email to {to}")
    except Exception as e:
        print(f"Error sending email: {e}")

    return True  # Optionally, return a value indicating success

@app.route("/")
def home():
    return "Welcome to the JDK'S Messaging System!"

@app.route("/sendmail")
def sendmail():
    to = request.args.get('sendmail')
    if to:
        send_email.delay(to)
        return f'Sending email to {to}...'
    else:
        return 'Error: Missing "sendmail" parameter.'

@app.route("/talktome")
def talktome():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f'Logged at {current_time}\n'
    log_file = '/var/log/messaging_system.log'  # Adjust path as needed
    with open(log_file, 'a') as f:
        f.write(log_message)
    return 'Logging message...'

@app.route('/log')
def get_log():
    try:
        with open('logs/messaging_system.log', 'r') as f:
            log_content = f.read()
        return Response(log_content, mimetype='text/plain')
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True)