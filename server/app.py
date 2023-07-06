from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# @app.before_request
# def set_content_type():
#     if not request.headers.get('Content-Type'):
#         request.headers['Content-Type'] = 'application/json'

@app.route('/messages', methods = ["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by('created_at').all()
        messages_serialized = [message.to_dict() for message in messages]
        response = make_response(
            jsonify(messages_serialized),
            200
        )
        
    elif request.method == "POST":
        data = request.get_json()
        new_message = Message(
            body = data['body'],
            username = data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        response = make_response(
            jsonify(message_dict),
            201
        )
       
    return response

@app.route('/messages/<int:id>', methods = ["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == "PATCH":
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        db.session.add(attr)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200
        )
        
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        response = make_response(
            jsonify({'deleted': True}),
            200,
        )
        
    return response
if __name__ == '__main__':
    app.run(port=5555)
