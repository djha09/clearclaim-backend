from flask import Flask, request, jsonify
from flask_cors import CORS
from simplify_pdf import simplify_policy_pdf
from rebuttal import generate_rebuttal_from_pdf, generate_rebuttal_from_text
from read_pdf import read_pdf_file
from verify import verify_from_pdf
import os

app = Flask(__name__)
CORS(app)

@app.route("/simplify_pdf", methods=["POST"])
def simplify_pdf_route():
    file = request.files.get("pdf")
    if not file:
        return jsonify({"error": "No PDF uploaded"}), 400

    filepath = f"temp_{file.filename}"
    file.save(filepath)

    try:
        result = simplify_policy_pdf(filepath)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Failed to simplify PDF: {str(e)}"}), 500
    finally:
        os.remove(filepath)

@app.route("/rebuttal", methods=["POST"])
def rebuttal_route():
    file = request.files.get("pdf")
    reason = request.form.get("reason", "")

    if file:
        filepath = f"temp_{file.filename}"
        file.save(filepath)
        try:
            pdf_text = read_pdf_file(filepath)
            response = generate_rebuttal_from_pdf(pdf_text, reason)
        except Exception as e:
            return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500
        finally:
            os.remove(filepath)
    elif reason:
        try:
            response = generate_rebuttal_from_text(reason)
        except Exception as e:
            return jsonify({"error": f"Failed to generate rebuttal: {str(e)}"}), 500
    else:
        return jsonify({"error": "No reason or file provided"}), 400

    return jsonify(response)

@app.route("/verify", methods=["POST"])
def verify_pdf():
    file = request.files.get("pdf")
    claim = request.form.get("claim", "")

    if not file or not claim:
        return jsonify({"error": "PDF and claim text are required"}), 400

    filepath = f"temp_{file.filename}"
    file.save(filepath)

    try:
        pdf_text = read_pdf_file(filepath)
        response = verify_from_pdf(pdf_text, claim)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': f"Failed to process PDF: {str(e)}"}), 500
    finally:
        os.remove(filepath)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's port or default to 10000
    app.run(host="0.0.0.0", port=port)
