from flask import Flask, render_template_string

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{{ name }} - Portfolio</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#0b1220;color:#e6edf3}
    header{padding:60px 20px;background:linear-gradient(135deg,#1f6feb,#7c3aed);color:white}
    .wrap{max-width:1000px;margin:0 auto;padding:0 20px}
    h1{margin:0 0 10px;font-size:42px}
    .sub{opacity:.95;margin:0 0 22px;font-size:18px}
    .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:20px;padding:25px 0}
    @media(max-width:860px){.grid{grid-template-columns:1fr}}
    .card{background:#111827;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:18px;box-shadow:0 10px 30px rgba(0,0,0,.2)}
    h2{margin-top:0}
    ul{padding-left:18px}
    a.btn{display:inline-block;margin-top:10px;background:white;color:#111827;padding:10px 14px;border-radius:10px;text-decoration:none;font-weight:700}
    .muted{opacity:.8}
    footer{padding:25px 20px;color:#94a3b8;text-align:center}
  </style>
</head>
<body>
  <header>
    <div class=wrap>
      <h1>{{ name }}</h1>
      <p class=sub>{{ tagline }}</p>
      <a class=btn href={{ cv_link }} target=\"_blank\" rel=\"noreferrer\">Download CV</a>
      <p class=muted style=\"margin-top:16px\">Location: {{ location }} | Email: <a style=\"color:white\" href=\"mailto:{{ email }}\">{{ email }}</a></p>
    </div>
  </header>

  <main class=wrap>
    <div class=grid>
      <section class=card>
        <h2>About</h2>
        <p class=muted>{{ about }}</p>

        <h2 style=\"margin-top:18px\">Skills</h2>
        <ul>
          {% for s in skills %}<li>{{ s }}</li>{% endfor %}
        </ul>

        <h2 style=\"margin-top:18px\">Projects</h2>
        <ul>
          {% for p in projects %}
            <li><b>{{ p.title }}</b> — <span class=muted>{{ p.desc }}</span> {% if p.link %}<a href={{ p.link }} target=\"_blank\" rel=\"noreferrer\">[link]</a>{% endif %}</li>
          {% endfor %}
        </ul>
      </section>

      <aside class=card>
        <h2>Quick Links</h2>
        <p class=muted>Replace these with your real profiles.</p>
        <p><a style=\"color:#60a5fa\" href={{ github }}>GitHub</a></p>
        <p><a style=\"color:#60a5fa\" href={{ linkedin }}>LinkedIn</a></p>
        <p><a style=\"color:#60a5fa\" href={{ website }}>Website</a></p>

        <h2 style=\"margin-top:18px\">Availability</h2>
        <p class=muted>{{ availability }}</p>
      </aside>
    </div>
  </main>

  <footer>
    <div>© {{ year }} {{ name }}. Built with Flask.</div>
  </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        INDEX_HTML,
        name="Your Name",
        tagline="Flask • Python • Web Apps",
        location="Your City",
        email="you@example.com",
        cv_link="https://example.com/your-cv.pdf",
        about="Write a short bio: what you do, what you enjoy building, and what you’re looking for.",
        skills=[
            "Python",
            "Flask",
            "JavaScript",
            "SQL",
            "HTML/CSS",
        ],
        projects=[
            {"title":"Project One","desc":"Short description of what it does.","link":"https://example.com"},
            {"title":"Project Two","desc":"Another short description.","link":""},
        ],
        github="https://github.com/yourusername",
        linkedin="https://linkedin.com/in/yourusername",
        website="https://yourwebsite.com",
        availability="Open to freelance / internships / full-time roles.",
        year=__import__('datetime').datetime.now().year,
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

