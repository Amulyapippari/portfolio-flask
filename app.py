import os
from flask import Flask, render_template, request, flash, redirect, send_from_directory
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "replace_with_a_secret_key")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

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
        msg["To"] = EMAIL_ADDRESS
        msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending email: {e}", "error")

        return redirect("/")
    return render_template("Untitled-1.html")

@app.route("/download-pdf")
def download_pdf():
    return send_from_directory("static", "amulya_p_ur-1.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=True)
