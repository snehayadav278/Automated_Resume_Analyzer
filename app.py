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
            <h2>Resume Score: {score}</h2>
            <h3>Matched Skills:</h3>
            {found_skills}
            <br><br>
            <a href="/">Upload Another Resume</a>
            """

    return """
    <h2>Upload Resume (PDF)</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="resume">
        <input type="submit" value="Upload">
    </form>
    """

if __name__ == '__main__':
    app.run(debug=True)