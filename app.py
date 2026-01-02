from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    substitutions = ""
    if request.method == 'POST':
        url = request.form.get('url')
        prompt = request.form.get('prompt')
        substitutions = f"你要改编URL: {url}\nP你的思路是: {prompt}"
        return render_template('index.html', substitutions=substitutions)
        
    
    return render_template('index.html', substitutions=substitutions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
