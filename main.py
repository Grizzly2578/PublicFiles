import os
import flask
import pathlib
import inspect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask import Flask, render_template_string, send_from_directory, url_for, render_template
from threading import Thread

os.chdir(os.path.dirname(os.path. abspath(inspect.getframeinfo(inspect.currentframe()).filename)))

app = Flask("0")
app.config['ROOT_FOLDER'] = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
app.config['UPLOAD_FOLDER'] = 'database\\Public Files'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['VIDEOS_FOLDER'] = str(pathlib.Path.home())+ '\\Videos'
app.config['SCRIPTS_FOLDER'] = 'js'
app.config['CSS_FOLDER'] = app.config['ROOT_FOLDER']+'\css'
BANNED_FILES = app.config['BANNED_FILES'] = ["ico", "ini"]
BANNED_FILES_MUSIC_FOLDER = app.config['BANNED_FILES_MUSIC_FOLDER'] = [
  "ico", 
  "ini", 
  "txt", 
  "bat", 
  "jpeg", 
  "png", 
  "jpg", 
  "webm",
  "webp",
  "py"
  ]
BANNED_FILES_VIDEOS_FOLDER = app.config['BANNED_FILES_VIDEOS_FOLDER'] = [
  "ico", 
  "ini", 
  "txt", 
  "bat", 
  "py",
  "srt"
  ]
app.config['MUSIC_FOLDER'] = str(pathlib.Path.home())+ '\\Music'



class UploadFileForm(FlaskForm):
  file = FileField("File", validators=[InputRequired()])
  submit = SubmitField("Upload File")

class none_form:
  def hidden_tag(self):
    return""
  def file(self):
    return""
  def submit(self):
    return""

def file_browser(req_path, BASE_DIR, ban_type):
  try:
    form = UploadFileForm()

      # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

      # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
      return flask.abort(404)

      # Check if path is a file and serve
    if os.path.isfile(abs_path):
      return flask.send_file(abs_path)

      # Show directory contents
    files = []
    for i in os.listdir(abs_path):
      if not i.endswith(tuple(ban_type)):
        files.append(i)
    if not flask.request.url.endswith("Public%20Files"):
      form=none_form()
    elif form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return flask.redirect(flask.request.url)
    
    if flask.request.url.lower().endswith("/"):
      return render_template('index.html', files=files, form=form)
    else:
      return render_template('_index.html', files=files, form=form)

  except FileNotFoundError:
    os.mkdir("database")
    os.mkdir("database/Files")
    return flask.redirect(location=url_for('home'))
  
@app.route('/music/<music>')
def music(music):
  return send_from_directory(app.config['MUSIC_FOLDER'], music)

@app.route('/js/<script>')
def js(script):
  return send_from_directory(app.config['SCRIPTS_FOLDER'], script)

@app.route('/css/<css>')
def css(css):
  return send_from_directory(app.config['CSS_FOLDER'], css)

@app.route('/favicon.ico', methods=['GET'])
def favicon():
  return flask.send_file("favicon.ico")

@app.route('/',defaults={'req_path': ''})
@app.route('/<path:req_path>', methods=['GET', 'POST'])
def home(req_path):
  return file_browser(
    req_path=req_path, 
    BASE_DIR=f"{str(pathlib.Path.home())}\\Desktop\\Python\\website\\database",
    ban_type=BANNED_FILES
    )

@app.route('/test', methods=['GET'])
def test():
  return render_template("test.html")

@app.route('/chess')
def chess():
  return render_template("chess.html")

@app.route('/music', methods=['GET'],defaults={'req_path': ''})
@app.route('/music/<path:req_path>', methods=['GET', 'POST'])
def music_(req_path):
  return file_browser(
    req_path=req_path, 
    BASE_DIR=app.config['MUSIC_FOLDER'],
    ban_type=BANNED_FILES_MUSIC_FOLDER
    )

@app.route('/videos',defaults={'req_path': ''})
@app.route('/videos/<path:req_path>', methods=['GET'])
def videos_(req_path):
  return file_browser(
    req_path=req_path, 
    BASE_DIR=app.config['VIDEOS_FOLDER'],
    ban_type=BANNED_FILES_VIDEOS_FOLDER
    )

app.run(host="0.0.0.0",port=80, debug=True)