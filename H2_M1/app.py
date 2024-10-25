from flask import Flask, render_template, request
from dotenv import load_dotenv
from model import runModels
import os
from werkzeug.utils import secure_filename

load_dotenv()

app =Flask(__name__, template_folder = 'templates', static_folder='static',static_url_path='/')

@app.route('/')
def index():
    return render_template('about.html', active = 'index')

@app.route('/milestone1', methods=["GET","POST"])
def interaction_1():
    if request.method == 'POST':
        f = request.files["imgFile"]
        file_name = secure_filename(f.filename)

        cwd = os.getcwd()
        upld_path = cwd+'/static/imgs/'+file_name
        img_path = 'imgs/'+file_name
        f.save(upld_path)

        (caption, story) = runModels(upld_path)
        

        return render_template('milestone1.html', active='interaction_1', imgPath=img_path, story=story, caption=caption)
    else:
        return render_template('milestone1.html', active='interaction_1')


if __name__ == '__main__':
    app.run(host='0.0.0.0')