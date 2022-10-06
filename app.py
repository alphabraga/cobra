from flask import Flask
from blueprint.users import blueprint as users
 
app = Flask(__name__)
app.register_blueprint(users) 


if __name__ == '__main__':
    app.run()