from flask import Flask, request, jsonify
from flask_cors import CORS
from simplify_pdf import simplify_policy_pdf
from rebuttal import generate_rebuttal_from_pdf, generate_rebuttal_from_text
from chatbot import ask_insurance_question
from risk_score import calculate_risk_score
from read_pdf import read_pdf_file
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


@app.route("/chatbot", methods=["POST"])
def chatbot_route():
    query = request.form.get("query")
    file = request.files.get("pdf")

    if not query:
        return jsonify({"error": "Missing query"}), 400

    pdf_text = ""
    if file:
        filepath = f"temp_{file.filename}"
        file.save(filepath)
        try:
            pdf_text = read_pdf_file(filepath)
        except Exception as e:
            return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 500
        finally:
            os.remove(filepath)

    try:
        reply = ask_insurance_question(query, pdf_text)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": f"Chatbot failed: {str(e)}"}), 500


@app.route("/risk_score", methods=["POST"])
def risk_score_route():
    file = request.files.get("pdf")
    if not file:
        return jsonify({"error": "Missing PDF"}), 400

    filepath = f"temp_{file.filename}"
    file.save(filepath)

    try:
        score = calculate_risk_score(filepath)
        return jsonify(score)
    except Exception as e:
        return jsonify({"error": f"Failed to calculate risk score: {str(e)}"}), 500
    finally:
        os.remove(filepath)


if __name__ == "__main__":
    app.run(debug=True)
