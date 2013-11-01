import os
import random, string
from flask import Flask, render_template, send_from_directory, redirect, request

app = Flask(__name__)

redirects = {}

def encode_url(url):
    encoding = ''.join(random.choice(string.lowercase) for _ in range(6))
    while encoding in redirects:
        #D.R.Y
        encoding = ''.join(random.choice(string.lowercase) for _ in range(6))
    redirects[encoding] = url
    return encoding

@app.route('/')
def index():
    return render_template('index.html')

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

