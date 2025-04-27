from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from main import generate_worksheet  # Your updated function!

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        grade = request.form['grade']
        difficulty = request.form['difficulty']
        num_questions = int(request.form['num_questions'])
        topic_focus = request.form['topic_focus']
        graphs = int(request.form['graphs'])

        pdf_path = generate_worksheet(subject, grade, difficulty, num_questions, topic_focus, graphs)

        return redirect('/preview')

    return render_template('form.html')

@app.route('/preview')
def preview():
    return render_template('preview.html')

@app.route('/download/<path:filename>')
def download(filename):
    # If downloading normally
    return send_file(os.path.join('outputs', filename), as_attachment=True)

@app.route('/view/<path:filename>')
def view_pdf(filename):
    # If viewing inside iframe
    return send_file(os.path.join('outputs', filename), mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
