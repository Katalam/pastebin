import os, mysql.connector, sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

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

def main(slug, header, filepath):
    db = get_db()
    c = db.cursor()

    c.execute('SELECT slug FROM pastebins \
               WHERE slug=%(s)s', { 's': slug })
    d = c.fetchone()
    if d is not None:
        print('Slug already taken.')
        db.close()
        sys.exit()

    data = read_file(filepath)

    c.execute('INSERT INTO pastebins (slug, header, code) \
               VALUES (%(s)s, %(h)s, %(f)s);',
               { 's': slug, 'h': header, 'f': data})
    db.commit()
    db.close()
    print('Success\n')
    print(slug)


def read_file(filename):
    with open(filename, 'rb') as f:
        d = f.read()
    return d

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: {0} <slug> <header> <filename>\nExample: {0} qotd "Quote of the day protocol c" qotd.c'.format(sys.argv[0]))
        sys.exit()
    
    if os.path.exists(sys.argv[3]):
        if os.stat(sys.argv[3]).st_size == 0:
            print('File is empty')
            sys.exit()
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('File not found')
    
