from flask import Flask, render_template, request
from datetime import datetime
import smtplib
import os

app = Flask(__name__)
OWN_EMAIL = os.environ.get("OWN_EMAIL")
OWN_PASSWORD = os.environ.get("OWN_PASSWORD")
TARGET_EMAIL = os.environ.get("TARGET_EMAIL")
port = int(os.environ.get('PORT', 5000))


@app.route('/')
def home():
    return render_template('index.html', year=datetime.now().year, title='')


@app.route('/about')
def about():
    return render_template('about.html', year=datetime.now().year, title='- About Me')


@app.route('/projects')
def projects():
    return render_template('projects.html', year=datetime.now().year, title='- Projects')


@app.route('/conatct-me', methods=["GET", "POST"])
def contact():
    is_sent = False
    if request.method == "POST":
        is_sent = True
        user_form = {
            'name': request.form["name"],
            'email': request.form["email"],
            'phone_number': request.form["number"],
            'message': request.form["message"],
        }
        send_email(user_form)
        return render_template('contact.html', year=datetime.now().year, title='- Contact Me',
                               sent=is_sent)
    return render_template('contact.html', year=datetime.now().year, title='- Contact Me', sent=is_sent)


def send_email(details):
    email_message = f"Subject:New Website Message from {details['name']}\n\nName: {details['name']}" \
                    f"\nEmail: {details['email']}\nPhone: {details['phone_number']}\nMessage:{details['message']}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, TARGET_EMAIL, email_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
