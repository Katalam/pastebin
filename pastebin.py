import os, mysql.connector, string, random
from flask import Flask, session, redirect, url_for, request, render_template, abort
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def get_db():
    db = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_DATABASE')
    )
    return db

# c = db.cursor()

@app.route('/', methods=['GET'])
def index():
    s = request.args.get('s')
    if s is None:
        return render_template('new.html', header="New Paste")

    db = get_db()
    c = db.cursor()

    c.execute('SELECT header, CONVERT(code USING utf8) FROM pastebins \
               WHERE slug=%(s)s', { 's': s })
    data = c.fetchone()
    if data is None:
        db.close()
        abort(404)

    db.close()
    if request.args.get('r'):
        return render_template('raw.html', header=data[0],
                                       code=data[1])
    return render_template('code.html', header=data[0],
                                       code=data[1])

@app.route('/', methods=['POST'])
def index_post():

    h = request.form.get('header')
    code = request.form.get('text')

    if h == '' or code == '':
        return render_template('new.html', header="New Paste")

    db = get_db()
    c = db.cursor()

    s = unqiue_slug()
    while not is_slug_unqiue(s):
        s = unqiue_slug()

    c.execute('INSERT INTO pastebins (slug, header, code) \
               VALUES (%(s)s, %(h)s, %(c)s)', { 's': s, 'h': h, 'c': code})

    db.commit()
    db.close()
    return redirect(url_for('index') + '?s={0}'.format(s))

@app.errorhandler(404)
def page_404(e):
    return render_template('404.html', header='404 Not found'), 404


def is_slug_unqiue(s):
    db = get_db()
    c = db.cursor()
    c.execute('SELECT header, CONVERT(code USING utf8) FROM pastebins \
               WHERE slug=%(s)s', { 's': s })
    d = c.fetchone()
    db.close()
    return d is None

def unqiue_slug():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(5))
