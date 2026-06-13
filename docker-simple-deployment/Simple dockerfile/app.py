from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Prajwal DevOps Portfolio</title>
    <style>
        body{
            font-family: Arial, sans-serif;
            background:#f4f4f4;
            margin:0;
            padding:0;
        }
        .container{
            width:80%;
            margin:auto;
            padding:20px;
        }
        .card{
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            margin-top:20px;
        }
        h1{
            color:#333;
        }
        .btn{
            display:inline-block;
            padding:10px 20px;
            background:#007bff;
            color:white;
            text-decoration:none;
            border-radius:5px;
        }
        ul{
            line-height:2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Prajwal B</h1>
            <h3>DevOps & Cloud Engineer</h3>

            <p>
                Passionate about AWS, Docker, Kubernetes,
                Jenkins, Terraform, Ansible and CI/CD automation.
            </p>

            <h2>Skills</h2>
            <ul>
                <li>AWS</li>
                <li>Docker</li>
                <li>Kubernetes</li>
                <li>Jenkins</li>
                <li>Terraform</li>
                <li>Ansible</li>
                <li>GitHub Actions</li>
                <li>Python</li>
            </ul>

            <h2>Projects</h2>
            <ul>
                <li>3-Tier Application Deployment on Kubernetes</li>
                <li>End-to-End DevSecOps CI/CD Pipeline</li>
                <li>AWS Infrastructure Automation using Terraform</li>
                <li>Docker CMD vs ENTRYPOINT Demo</li>
            </ul>

            <a class="btn" href="https://prajwaldev.space">
                Visit Portfolio
            </a>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)