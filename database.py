import os, mysql.connector
from dotenv import load_dotenv
load_dotenv()

db = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_DATABASE')
)

c = db.cursor()

user_sql = '''CREATE TABLE IF NOT EXISTS pastebins (
    slug VARCHAR(254) NOT NULL DEFAULT '',
    header VARCHAR(254) NOT NULL DEFAULT '',
    code LONGBLOB NOT NULL DEFAULT '',
    PRIMARY KEY (slug));
    '''

c.execute(user_sql)

db.commit()

print('Success')
