from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]
@app.route("/")
def welcome():
    return jsonify({"message": "Welcome to the Event Management API!"})

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    new_event = Event(id=len(events) + 1, title=data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Invalid input"}), 400

    for event in events:
        if event.id == event_id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    if not any(event.id == event_id for event in events):
        return jsonify({"error": "Event not found"}), 404

    events[:] = [event for event in events if event.id != event_id]
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)