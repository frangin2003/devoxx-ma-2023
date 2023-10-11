from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/report', methods=['GET'])
def get_report():
    try:
        with open('police-report.txt', 'r') as f:
            content = f.read()
        return jsonify({"content": content}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
