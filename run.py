from flask import Flask

app = Flask(__name__)

from views import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:troy@localhost/todoapp'

if __name__ == '__main__':
    app.run()
