from flask import Flask, request
import pdfplumber

app = Flask(__name__)

required_skills = ["python", "java", "sql"]

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file = request.files['resume']

        if file:
            text = ""

            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    if page.extract_text():
                        text += page.extract_text()

            text = text.lower()

            score = 0
            found_skills = []

            for skill in required_skills:
                if skill in text:
                    score += 10
                    found_skills.append(skill)

            return f"""
            <html>
            <head>
                <title>Resume Analyzer</title>
                <style>
                    body {{
                        margin: 0;
                        font-family: 'Segoe UI', sans-serif;
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }}

                    .card {{
                        background: rgba(255, 255, 255, 0.15);
                        backdrop-filter: blur(15px);
                        padding: 40px;
                        border-radius: 20px;
                        text-align: center;
                        width: 400px;
                        color: white;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                    }}

                    h1 {{
                        margin-bottom: 10px;
                        font-size: 26px;
                    }}

                    .score {{
                        font-size: 40px;
                        font-weight: bold;
                        margin: 20px 0;
                        color: #00ffcc;
                    }}

                    .skills {{
                        margin-top: 20px;
                    }}

                    .skill-tag {{
                        display: inline-block;
                        background: white;
                        color: #333;
                        padding: 8px 15px;
                        margin: 5px;
                        border-radius: 20px;
                        font-size: 14px;
                        font-weight: 500;
                    }}

                    a {{
                        display: inline-block;
                        margin-top: 25px;
                        padding: 10px 20px;
                        background: white;
                        color: #764ba2;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: 600;
                        transition: 0.3s;
                    }}

                    a:hover {{
                        background: #f1f1f1;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>Resume Analysis Complete 🚀</h1>
                    <div class="score">{score}/30</div>

                    <div class="skills">
                        <h3>Matched Skills</h3>
                        {''.join(f'<span class="skill-tag">{skill}</span>' for skill in found_skills)}
                    </div>

                    <a href="/">Analyze Another Resume</a>
                </div>
            </body>
            </html>
            """

    return """
    <html>
    <head>
        <title>Resume Analyzer</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .card {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(15px);
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                width: 400px;
                color: white;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            }

            h1 {
                margin-bottom: 20px;
                font-size: 26px;
            }

            input[type="file"] {
                margin: 20px 0;
                padding: 10px;
                background: white;
                border-radius: 10px;
                border: none;
                width: 100%;
            }

            input[type="submit"] {
                padding: 12px 25px;
                background: #00ffcc;
                border: none;
                border-radius: 25px;
                font-weight: bold;
                cursor: pointer;
                transition: 0.3s;
            }

            input[type="submit"]:hover {
                background: #00ddb3;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>AI Resume Analyzer</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="resume" required>
                <br>
                <input type="submit" value="Analyze Resume">
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
