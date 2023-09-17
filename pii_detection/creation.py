import os

# Create necessary directories
os.makedirs('my_flask_app/templates', exist_ok=True)
os.makedirs('my_flask_app/static', exist_ok=True)

# Create the main Flask app script
app_script_content = """
from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

# Load the model
nlp = pipeline("ner", model="beki/en_spacy_pii_distilbert", tokenizer="beki/en_spacy_pii_distilbert")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    text = request.form['text']

    if not text:
        return "No text provided", 400

    results = nlp(text)
    contains_pii = any([result['entity'].startswith('PII') for result in results])

    return render_template('result.html', contains_pii=contains_pii, results=results)

if __name__ == '__main__':
    app.run()
"""

with open('my_flask_app/app.py', 'w') as f:
    f.write(app_script_content)

# Create the home page template
index_html_content = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>PII Analyzer</title>
  </head>
  <body>
    <div class="container">
        <h1 class="mt-5">PII Analyzer</h1>
        <form action="/analyze" method="post" class="mt-3">
            <div class="mb-3">
                <textarea name="text" class="form-control" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Analyze</button>
        </form>
    </div>
  </body>
</html>
"""

with open('my_flask_app/templates/index.html', 'w') as f:
    f.write(index_html_content)

# Create the result page template
result_html_content = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Analysis Result</title>
  </head>
  <body>
    <div class="container">
        <h1 class="mt-5">Analysis Result</h1>
        <p class="mt-3"><strong>Contains PII:</strong> {{ contains_pii }}</p>
        <p><strong>Details:</strong> {{ results }}</p>
        <a href="/" class="btn btn-secondary mt-3">Back</a>
    </div>
  </body>
</html>
"""

with open('my_flask_app/templates/result.html', 'w') as f:
    f.write(result_html_content)

print("Your Flask app has been set up in the 'my_flask_app' directory.")
