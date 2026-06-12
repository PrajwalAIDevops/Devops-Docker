from __future__ import annotations

import os
from flask import Flask, render_template, request


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/projects")
    def projects():
        # In a real app, this could come from a CMS or database.
        return render_template("projects.html")

    @app.get("/contact")
    def contact_get():
        return render_template("contact.html", status=None, form_data=None)

    @app.post("/contact")
    def contact_post():
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        message = (request.form.get("message") or "").strip()

        # Lightweight demo: do not send email automatically.
        # For production: integrate with SendGrid/SES or your preferred provider.
        status = None
        if name and email and message:
            status = "Thanks! Your message was received (demo)."
        else:
            status = "Please fill in all fields."

        form_data = {"name": name, "email": email, "message": message}
        return render_template("contact.html", status=status, form_data=form_data)

    return app


app = create_app()


if __name__ == "__main__":
    # Local dev defaults
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")

