import os, mysql.connector
from flask import Flask, session, redirect, url_for, request, render_template
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
# db.close()

@app.route('/')
def index():
    s = request.args.get('s')
    if s is None:
        return render_template('base.html')

    db = get_db()
    c = db.cursor()

    c.execute('SELECT header, CONVERT(code USING utf8) FROM pastebins \
               WHERE slug=%(s)s', { 's': s })
    data = c.fetchone()
    if data is None:
        return render_template('404.html', header='404 Not found')

    db.close()
    if request.args.get('r'):
        return render_template('raw.html', header=data[0],
                                       code=data[1])
    return render_template('code.html', header=data[0],
                                       code=data[1])
