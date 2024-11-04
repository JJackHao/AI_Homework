from flask import Flask, render_template, request
from dotenv import load_dotenv
from model_milestone1 import runModels
from model_milestone2 import runModels_langchain, runModels_langchain_RAG

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

@app.route('/milestone2', methods=["GET","POST"])
def interaction_2():
    if request.method == 'POST':
        f = request.files["imgFile"]
        file_name = secure_filename(f.filename)
        cwd = os.getcwd()
        upld_path = cwd+'/static/imgs/'+file_name
        img_path = 'imgs/'+file_name
        f.save(upld_path)

        # db_dir = os.path.join(cwd,"chroma_db")

        story_style = request.form.get('storyRadioOptions')
        # print(f"the story style selcted is {story_style}")

        (caption, story) = runModels_langchain(upld_path,story_style)
        # (caption, story) = runModels_langchain_RAG(upld_path,story_style,db_dir)

        

        return render_template('milestone2.html', active='interaction_2', imgPath=img_path, story=story, caption=caption, style=story_style)
    else:
        return render_template('milestone2.html', active='interaction_2')



if __name__ == '__main__':
    app.run(host='0.0.0.0')