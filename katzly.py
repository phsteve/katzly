import os
import random, string
from urlparse import urlparse
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Required, URL
from flask import Flask, render_template, send_from_directory, redirect, request

app = Flask(__name__)
app.config.from_object('config')
#from app import views

class URLForm(Form):
    url = StringField('url', validators = [DataRequired(), Required(message="Please enter a URL."), URL(message="Please enter a valid URL.")])

redirects = {}

def encode_url(url):
    encoding = ''.join(random.choice(string.lowercase) for _ in range(6))
    while encoding in redirects: #in case there's repeats (1/308915776 chance!)
        #D.R.Y
        encoding = ''.join(random.choice(string.lowercase) for _ in range(6))
    redirects[encoding] = url
    return encoding

def parse_url(url):
    u = urlparse(url)
    if not u.scheme:
        url = 'http://' + url
    return url

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = URLForm(request.form)
    if form.validate_on_submit():
        return redirect('/shortened')
    # if request.method == 'GET':
    #     return render_template('index.html')
    # else:
    #     url = request.form['url']
    #     if url:
    return render_template('index.html', form=form)


@app.route('/shortened', methods = ['GET', 'POST'])
def shortened():
    if request.method == 'POST':
        url = request.form['url']
        encoding = encode_url(url) 
    return render_template('shortened.html', url=url, encoding=encoding)

@app.route('/<encoding>')
def redir(encoding):
    return redirect(redirects[encoding])

@app.route('/encodings')
def encodings():
    return render_template('encodings.html', redirects=redirects)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

