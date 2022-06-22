import logging
import os
from re import template
from flask import (
    Flask,render_template,url_for, current_app, g, request, redirect, flash
)
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD1234"
app.logger.setLevel(logging.DEBUG)

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)


@app.route("/contact")
def index():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        descryption = request.form["descryption"]
        

        is_valid= True
        if not username:
            flash("ユーザ名は必須です")
            is_valid = False
        if not email:
            flash("メールアドレスは必須です")
            is_valid = False
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False
        
        if not descryption:
            flash("問い合わせ内容は必須です")
            is_valid = False
        if not is_valid:
            return render_template("contact.html")

        flash("問い合わせ内容はメールにて送信しました。")
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username = username,
            descryption = descryption
        )
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")


def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients = [to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)

    mail.send(msg)
