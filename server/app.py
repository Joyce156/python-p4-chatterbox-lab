from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message  # import the model from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

# Initialize the database before migrations
db.init_app(app)
migrate = Migrate(app, db)


# ---------------- ROUTES ---------------- #

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([m.to_dict() for m in messages]), 200

    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    data = request.get_json()
    message.body = data.get('body')
    db.session.commit()
    return jsonify(message.to_dict()), 200


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    db.session.delete(message)
    db.session.commit()
    return {}, 204


# ---------------- RUN APP ---------------- #
if __name__ == '__main__':
    app.run(port=5555)
