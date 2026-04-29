from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our modular services
from name_dedup import process_duplicates
from gender_names import process_gender

app = Flask(__name__)
CORS(app)  # Allow Excel (localhost) to talk to Flask

@app.route('/detect_duplicates', methods=['POST'])
def detect_duplicates():
    """
    Expects JSON: { "data": [ [row_idx, "Name A"], ... ], "threshold": 0.90 }
    """
    content = request.json
    raw_data = content.get('data',[])
    threshold = float(content.get('threshold', 0.90))

    if not raw_data:
        return jsonify({"groups":[]})

    try:
        groups = process_duplicates(raw_data, threshold)
        return jsonify({"groups": groups})
    except Exception as e:
        print(f"Error in deduplication: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict_gender', methods=['POST'])
def predict_gender():
    """
    Expects JSON: { "data": [[row_idx, "Name A"], ... ] }
    """
    content = request.json
    raw_data = content.get('data', [])

    if not raw_data:
        return jsonify({"results":[]})

    try:
        results = process_gender(raw_data)
        return jsonify({"results": results})
    except Exception as e:
        print(f"Error in gender prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)