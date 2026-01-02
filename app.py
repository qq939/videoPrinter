from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


import pipeline

@app.route('/', methods=['GET', 'POST'])
def index():
    substitutions = ""
    video_url = None
    if request.method == 'POST':
        url = request.form.get('url')
        prompt = request.form.get('prompt')
        
        # Run the full pipeline
        # This will block until completion
        try:
            output_path = pipeline.run_pipeline(url, prompt)
            
            # Read the generated script to show in the UI
            if os.path.exists('scripts/1video_description.txt'):
                with open('scripts/1video_description.txt', 'r', encoding='utf-8') as f:
                    substitutions = f.read()
            else:
                substitutions = "Pipeline finished, but description file not found."

            if output_path and os.path.exists(output_path):
                video_url = url_for('static', filename='output.mp4')
                
        except Exception as e:
            substitutions = f"Error during pipeline execution: {str(e)}"
        
        return render_template('index.html', substitutions=substitutions, video_url=video_url)
        
    
    return render_template('index.html', substitutions=substitutions, video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
