from flask import Flask, render_template, request, flash, redirect
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv 

app = Flask(__name__)
app.secret_key = "replace_with_a_secret_key"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS =  os.getenv("EMAIL_USER")         # your Gmail address
EMAIL_PASSWORD =os.getenv("EMAIL_PASS")           # the 16-char App Password from Google

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields are required.", "error")
            return redirect("/")

        msg = EmailMessage()
        msg["Subject"] = f"New Contact Message from {name}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS  # send to yourself
        msg.set_content(
            f"Name: {name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending email: {e}", "error")

        return redirect("/")
    return render_template("Untitled-1.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
