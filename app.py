import os
from flask import Flask, render_template, request, flash, redirect, send_from_directory
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file (only for local development)
if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key-change-this")

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        # Validate form fields
        if not name or not email or not message:
            flash("All fields are required.", "error")
            return redirect("/")
        
        # Check if email credentials are configured
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            flash("Server configuration error. Please contact administrator.", "error")
            print("ERROR: EMAIL_USER or EMAIL_PASS not set in environment variables")
            return redirect("/")
        
        # Create email message
        msg = EmailMessage()
        msg["Subject"] = f"New Contact Message from {name}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        
        # Send email
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            flash("Your message has been sent successfully!", "success")
            print(f"SUCCESS: Email sent from {name} ({email})")
        except smtplib.SMTPAuthenticationError:
            flash("Authentication failed. Please try again later.", "error")
            print("ERROR: SMTP Authentication failed - check EMAIL_USER and EMAIL_PASS")
        except smtplib.SMTPException as e:
            flash("Failed to send email. Please try again later.", "error")
            print(f"SMTP ERROR: {e}")
        except Exception as e:
            flash("An error occurred. Please try again later.", "error")
            print(f"ERROR: {e}")
        
        return redirect("/")
    
    return render_template("Untitled-1.html")

@app.route("/download-pdf")
def download_pdf():
    return send_from_directory("static", "amulya_p_ur-1.pdf", as_attachment=True)

if __name__ == "__main__":
    # For local development only
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=True)