from flask import Blueprint, request, jsonify
from .openai_service import generate_email
from .utils import save_draft, get_drafts

main = Blueprint("main", __name__)

# No longer using hardcoded scenarios, so we remove SCENARIOS

@main.route("/generate-email", methods=["POST"])
def generate_email_route():
    data = request.get_json()
    transcript = data.get("transcript")
    scenario = data.get("scenario")  # This is the feedback used for improving the draft

    # Log received data
    print("Received transcript:", transcript)
    print("Received scenario (feedback):", scenario)

    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    # Check if it's the first draft generation or improvement
    if scenario == "Generated Draft":
        # First draft generation
        print("Generating the initial draft...")
        email = generate_email(transcript, "Generate Draft")
    else:
        # Improving the existing draft
        print("Improving the draft based on feedback...")
        email = generate_email(transcript, scenario)  # Use the feedback (scenario) to improve the draft

    # Save the draft for further improvements
    save_draft(scenario, transcript, email)

    return jsonify({"email": email})

@main.route("/drafts", methods=["GET"])
def list_drafts():
    # Returns all the drafts stored
    return jsonify(get_drafts())
