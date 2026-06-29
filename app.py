from flask import Flask, jsonify, request

app = Flask(__name__)


# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Helper function to find an event
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event

    return None


# POST /events
# Create a new event
@app.route("/events", methods=["POST"])
def create_event():

    # Get JSON data from request
    data = request.get_json()

    # Validate input
    if not data or "title" not in data:
        return jsonify({
            "error": "Title is required"
        }), 400


    # Generate new ID
    new_id = len(events) + 1


    # Create Event object
    new_event = Event(
        new_id,
        data["title"]
    )


    # Store event
    events.append(new_event)


    # Return response
    return jsonify({
        "message": "Event created successfully",
        "event": new_event.to_dict()
    }), 201



# PATCH /events/<id>
# Update event title
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):

    # Find event
    event = find_event(event_id)


    # Check if exists
    if not event:
        return jsonify({
            "error": "Event not found"
        }), 404


    # Get JSON data
    data = request.get_json()


    # Validate title
    if not data or "title" not in data:
        return jsonify({
            "error": "Title is required"
        }), 400


    # Update title
    event.title = data["title"]


    return jsonify({
        "message": "Event updated successfully",
        "event": event.to_dict()
    }), 200



# DELETE /events/<id>
# Remove event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    # Find event
    event = find_event(event_id)

    # Check if exists
    if not event:
        return jsonify({
            "error": "Event not found"
        }), 404

    # Remove event
    events.remove(event)
    return jsonify({
        "message": "Event deleted successfully"
    }), 200
if __name__ == "__main__":
    app.run(debug=True, port=5555)