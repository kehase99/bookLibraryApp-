from email.mime.text import MIMEText
import os
import smtplib
from app.config.email import SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD
from jinja2 import Environment, FileSystemLoader


def render_email_template(template_name: str, context: dict) -> str:
    templates_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "email_templates")
    )
    env = Environment(loader=FileSystemLoader(templates_path))
    try:
        template = env.get_template(template_name)
        rendered = template.render(context)
        if not rendered or not isinstance(rendered, str):
            raise ValueError(
                f"Template {template_name} rendered an invalid or empty result."
            )
        return rendered
    except Exception as e:
        print(f"Error rendering template {template_name}: {str(e)}")
        return ""


def send_registration_email(to_email, full_name, username, password):
    try:
        if not all(
            [
                to_email,
                full_name,
                username,
                password,
                SMTP_SERVER,
                SMTP_PORT,
                SMTP_EMAIL,
                SMTP_PASSWORD,
            ]
        ):
            raise ValueError(
                "One or more required parameters or config variables are missing."
            )

        email_body = render_email_template(
            "registration_email_template.html",
            {"full_name": full_name, "username": username, "password": password},
        )

        if not isinstance(email_body, str) or not email_body.strip():
            raise ValueError("Rendered email body is empty or invalid.")

        msg = MIMEText(email_body, "html", _charset="utf-8")
        msg["From"] = SMTP_EMAIL  # Updated to SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Welcome to My Library"

        server = smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT))
        server.starttls()
        server.login(
            SMTP_EMAIL, SMTP_PASSWORD
        )  # Updated to SMTP_EMAIL and SMTP_PASSWORD
        server.send_message(msg)
        server.quit()

        print(f"Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
