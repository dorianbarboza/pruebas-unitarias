from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://dorian:pass12345@localhost/unitarias'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))

    def serialize(self):
        return {
                'id', self.id,
                'username', self.username,
                'password', self.password
                }

@app.route('/get_users')
def get_all_users():
    users = User.query.all()
    return jsonify({
    [user.serialize() for user in users]
    }), 200

@app.route('/post_users', methods=['POST'])
def post_user():
    username = request.form['username']
    password = request.form['password']
    new_user=User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return {'message':'done'}, 201
    

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
